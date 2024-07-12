import os
from flask import (
    Flask, flash, render_template,
    send_from_directory, jsonify,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import certifi
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import timedelta, datetime
import cloudinary
import cloudinary.uploader
import cloudinary.api

# Cloudinary configuration
import config

# Checking if env.py file exists for environment variables
if os.path.exists("env.py"):
    import env

# Creating Flask application instance
app = Flask(__name__)

# Configuration for MongoDB connection using environment variables
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")
app.config["CLOUDINARY_URL"] = os.environ.get("CLOUDINARY_URL")
app.config["UPLOAD_FOLDER"] = os.path.join(os.getcwd(), 'static/uploads')


# Initializing PyMongo with Flask application instance with certifi
mongo = PyMongo(app, tlsCAFile=certifi.where())

# Session configuration
app.config["SESSION_PERMANENT"] = False  # Session is not permanent by default
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=30)


@app.route("/")
def index():
    # Render the main index page
    return render_template('index.html')


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        # Get form data
        name = request.form.get("name")
        gender = request.form.get("gender")
        dob = request.form.get("dob")  # Get date of birth
        phone = request.form.get("phone")
        # Convert email to lower case
        email = request.form.get("email").lower()
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        # Check if the email already exists
        existing_user = mongo.db.users.find_one({"email": email})
        if existing_user:
            flash(
                "Email already exists. Please use a different email.", "danger"
            )
            return redirect(url_for("signup"))

        # Check if passwords match
        if password == confirm_password:
            # Hash the password
            hashed_password = generate_password_hash(password)
            # Create a new user record
            new_user = {
                "name": name,
                "gender": gender,
                "dob": dob,  # Save date of birth
                "phone": phone,
                "email": email,
                "password": hashed_password,
                "role": "patient"  # Assign role
            }
            # Insert the new user into the database
            mongo.db.users.insert_one(new_user)
            flash("Registration successful!", "success")

            # Log the user in by adding their email to the session
            session["user"] = email

            return redirect(url_for("profile", username=email))
        else:
            flash("Passwords do not match. Please try again.", "danger")
            return redirect(url_for("signup"))

    # Render the signup template
    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Get form data
        email = request.form.get("email").lower()
        password = request.form.get("password")
        remember = request.form.get("remember")
        # Find the user by email
        existing_user = mongo.db.users.find_one({"email": email})

        if not existing_user:
            # If not found in users, check in doctors collection
            existing_user = mongo.db.doctors.find_one({"email": email})

        if existing_user:
            # Check if the password matches
            if check_password_hash(existing_user["password"], password):
                session["user"] = email
                flash("Welcome, {}".format(existing_user["name"]), "success")

                # Set session to be permanent if remember me is checked
                if remember:
                    # This sets the session to use the permanent lifetime
                    session.permanent = True
                    # Set session lifetime to 30 days
                    app.permanent_session_lifetime = timedelta(days=30)

                return redirect(url_for("profile", username=email))
            else:
                flash("Incorrect Email and/or Password", 'danger')
                return redirect(url_for("login"))

        else:
            flash("Incorrect Email and/or Password", 'danger')
            return redirect(url_for("login"))
    # Render the login template
    return render_template("login.html")


def generate_image_name(full_name):
    return full_name.lower().replace(" ", "-")

@app.route("/add_doctor", methods=["GET", "POST"])
def add_doctor():
    if "user" in session and mongo.db.users.find_one({"email": session["user"], "role": "admin"}):
        if request.method == "POST":
            name = request.form.get("name")
            email = request.form.get("email")
            specialty = request.form.get("specialty")
            description = request.form.get("description")
            additional_info = request.form.get("additional_info")
            password = request.form.get("password")

            # Hash the password
            hashed_password = generate_password_hash(password)

            # Generate image name
            image_name = generate_image_name(name)

            # Create a new doctor record
            new_doctor = {
                "name": name,
                "email": email,
                "specialty": specialty,
                "description": description,
                "additional_info": additional_info,
                "image": image_name,  # Automatically generated image name
                "password": hashed_password,  # Save the hashed password
                "role": "doctor"  # Assign the role of doctor
            }

            # Insert the new doctor into the collection
            mongo.db.doctors.insert_one(new_doctor)

            flash("Doctor added successfully!", "success")
            return redirect(url_for("doctors"))
        
        return render_template("add_doctor.html")
    else:
        flash("You do not have permission to access this page.", "danger")
        return redirect(url_for("index"))
    

@app.route("/logout")
def logout():
    # Remove user from session
    session.pop("user", None)
    flash("You have been logged out.", 'info')
    response = redirect(url_for("index"))

    # Prevent caching of this response
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'

    # For HTTP/1.0 backward compatibility
    response.headers['Pragma'] = 'no-cache'

    # Expire the content immediately
    response.headers['Expires'] = '0'
    return response


@app.route("/doctors")
def doctors():
    doctors_list = mongo.db.doctors.find()
    return render_template("doctors.html", doctors=doctors_list)

@app.context_processor
def utility_processor():
    def get_image_path(image_name):
        return f"images/doctors/{image_name}-600.webp"
    return dict(get_image_path=get_image_path)


@app.route("/policy")
def policy():
    return render_template("policy.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/profile/<username>")
def profile(username):
    """ Show the profile for that user."""
    try:
        # Найдите пользователя по email
        user = mongo.db.users.find_one({"email": username})

        if not user:
            # Если не найден в users, проверьте в коллекции doctors
            user = mongo.db.doctors.find_one({"email": username})
        
        if user:
            # Получите текущего пользователя из сессии
            current_email = session.get("user")
            current_user = mongo.db.users.find_one({"email": current_email})

            # Проверьте, является ли текущий пользователь администратором, просматривающим другой профиль
            viewing_as_admin = current_user and current_user["role"] == "admin" and current_email != username

            # Получите медицинские записи пользователя
            medical_records = list(
                mongo.db.medical_records.find({"patient_id": user["_id"]})
            )
            # Получите записи о приёмах пользователя
            appointments = list(
                mongo.db.appointments.find({"patient_id": user["_id"]})
            )
            # Получите загруженные файлы пользователя
            user_files = list(
                mongo.db.user_files.find({"user_id": user["_id"]})
            )
            # Отрендерите шаблон профиля с данными пользователя
            return render_template(
                "profile.html",
                user=user,
                medical_records=medical_records,
                appointments=appointments,
                user_files=user_files,
                role=current_user["role"] if viewing_as_admin else user["role"],
                viewing_as_admin=viewing_as_admin
            )
        else:
            flash("User not found", "danger")
            return redirect(url_for("index"))
    except Exception as e:
        flash(str(e), "danger")
        return redirect(url_for("index"))


@app.route("/edit_user_ajax", methods=["POST"])
def edit_user_ajax():
    if "user" in session:
        current_email = session["user"]
        print(f"Current user email: {current_email}")  # Debugging statement
        current_user = mongo.db.users.find_one(
            {"email": current_email}
        ) or mongo.db.doctors.find_one(
            {"email": current_email}
        )
        if current_user:
            user_id = request.json.get("user_id")
            print(f"Target user ID: {user_id}")  # Debugging statement
            user = mongo.db.users.find_one(
                {"_id": ObjectId(user_id)}
            ) or mongo.db.doctors.find_one(
                {"_id": ObjectId(user_id)}
            )

            if user:
                print(f"Found target user: {user['email']}")  # Debugging statement
                if current_user["role"] != "admin":
                    current_password = request.json.get("current_password")
                    print("Current password provided")  # Debugging statement

                    # Verify current password
                    if not check_password_hash(user["password"], current_password):
                        print("Incorrect current password")  # Debugging statement
                        return {
                            "success": False, 
                            "message": "Current password is incorrect."
                        }, 403

                # Get form data
                name = request.json.get("name")
                gender = request.json.get("gender")
                dob = request.json.get("dob")
                phone = request.json.get("phone")
                new_email = request.json.get("email").lower()

                # Update data dictionary
                update_data = {
                    "name": name,
                    "gender": gender,
                    # Ensure dob is not null
                    "dob": dob if dob else user.get("dob"),
                    "phone": phone,
                    "email": new_email,
                }

                # Allow role change only for admin users
                if current_user["role"] == "admin":
                    role = request.json.get("role")
                    # Ensure role is not null
                    update_data["role"] = role if role else user.get("role")

                # Update user information in the database
                if "role" in user and user["role"] == "doctor":
                    mongo.db.doctors.update_one(
                        {"_id": user["_id"]},
                        {"$set": update_data}
                    )
                else:
                    mongo.db.users.update_one(
                        {"_id": user["_id"]},
                        {"$set": update_data}
                    )

                # Update session email if admin is editing their own profile and email changed
                if current_user["_id"] == user["_id"] and current_email != new_email:
                    session["user"] = new_email
                    flash(
                        "Your email has been updated to {}.".format(new_email),
                        "success"
                    )
                    return {
                        "success": True, 
                        "message": "Your email has been updated.",
                        "redirect": url_for("profile", username=new_email)
                    }
                else:
                    flash("User information has been updated.", "success")
                    return {
                        "success": True, 
                        "message": "User information has been updated.",
                        "redirect": url_for("profile", username=current_email)
                    }
            else:
                print("User not found")  # Debugging statement
                return {"success": False, "message": "User not found."}, 404
        else:
            print("Current user not found")  # Debugging statement
            return {"success": False, "message": "Current user not found."}, 404
    else:
        print("Not logged in")  # Debugging statement
        return {
            "success": False, 
            "message": "You need to log in to edit user information."
        }, 403


@app.route("/upload_file_ajax", methods=["POST"])
def upload_file_ajax():
    if "user" in session:
        file = request.files.get("file")
        file_type = request.form.get("file_type")
        user_id = request.form.get("user_id")

        if file and allowed_file(file.filename):
            result = cloudinary.uploader.upload(file)

            file_url = result['secure_url']
            file_id = result['public_id']
            file_name = secure_filename(file.filename)

            new_file = {
                "user_id": ObjectId(user_id),
                "file_id": file_id,
                "file_url": file_url,
                "file_name": file_name,
                "file_type": file_type,
                "uploaded_at": datetime.utcnow()
            }
            mongo.db.user_files.insert_one(new_file)

            return jsonify({
                "success": True,
                "message": "File uploaded successfully.",
                "file_id": file_id,
                "file_url": file_url,
                "file_name": file_name
            })
        else:
            return jsonify({
                "success": False,
                "message": "Invalid file type."
            }), 400
    else:
        return jsonify({
            "success": False,
            "message": "You need to log in to upload files."
        }), 403

@app.route("/delete_file", methods=["POST"])
def delete_file():
    if "user" in session:
        file_id = request.form.get("file_id")
        print(f"Received request to delete file with ID: {file_id}")
        if file_id:
            if delete_from_cloudinary(file_id):
                file_record = mongo.db.user_files.find_one({"file_id": file_id})
                if file_record:
                    result = mongo.db.user_files.delete_one({"file_id": file_id})
                    print(f"Database deletion result: {result.deleted_count} document(s) deleted.")
                    if result.deleted_count > 0:
                        return jsonify({"success": True, "message": "File deleted successfully."})
                    else:
                        return jsonify({"success": False, "message": "File deleted from Cloudinary but not found in the database."})
                else:
                    return jsonify({"success": False, "message": "File not found in the database."})
            else:
                return jsonify({"success": False, "message": "Failed to delete the file from Cloudinary."})
        else:
            return jsonify({"success": False, "message": "File ID is required."})
    else:
        return jsonify({"success": False, "message": "You need to log in to delete files."})

def delete_from_cloudinary(file_id):
    try:
        result = cloudinary.uploader.destroy(file_id)
        print(f"Cloudinary deletion result: {result}")
        return result.get("result") == "ok"
    except Exception as error:
        print(f"An error occurred: {error}")
        return False

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "pdf", "doc", "docx"}
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/admin/users")
def admin_users():
    if "user" in session and mongo.db.users.find_one({"email": session["user"], "role": "admin"}):
        users = list(mongo.db.users.find())
        doctors = list(mongo.db.doctors.find())
        return render_template("admin_users.html", users=users, doctors=doctors)
    else:
        flash("You do not have permission to access this page.", "danger")
        return redirect(url_for("index"))


@app.route("/admin/patients")
def admin_patients():
    if "user" in session and mongo.db.users.find_one({"email": session["user"], "role": "admin"}):
        patients = mongo.db.users.find({"role": "patient"})
        return render_template("admin_patients.html", patients=patients)
    else:
        flash("You do not have permission to access this page.", "danger")
        return redirect(url_for("index"))

@app.route("/admin/doctors")
def admin_doctors():
    if "user" in session and mongo.db.users.find_one({"email": session["user"], "role": "admin"}):
        doctors = mongo.db.doctors.find()
        return render_template("admin_doctors.html", doctors=doctors)
    else:
        flash("You do not have permission to access this page.", "danger")
        return redirect(url_for("index"))


if __name__ == "__main__":
    # Run the Flask application
    app.run(
        host=os.environ.get("IP"), port=int(os.environ.get("PORT")), debug=True
    )