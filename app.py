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
from datetime import timedelta, datetime, timezone
import cloudinary
import cloudinary.uploader
import cloudinary.api
import secrets
import string
import re

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
        email = request.form.get("email").lower()
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        # Check if the email already exists
        existing_user = mongo.db.users.find_one({"email": email})
        if existing_user:
            flash("Email already exists. Please use a different email.", "danger")
            return redirect(url_for("signup"))

        # Check if passwords match
        if password != confirm_password:
            flash("Passwords do not match. Please try again.", "danger")
            return redirect(url_for("signup"))

        # Validate password requirements
        if not re.match(r"(?=.*\d)(?=.*[A-Z]).{8,}", password):
            flash("Password must contain at least 8 characters, including UPPER/lowercase and numbers", "danger")
            return redirect(url_for("signup"))

        # Hash the password
        hashed_password = generate_password_hash(password)
        # Create a new user record
        new_user = {
            "name": name,
            "gender": gender,
            "dob": dob,
            "phone": phone,
            "email": email,
            "password": hashed_password,
            "role": "patient"
        }
        # Insert the new user into the database
        mongo.db.users.insert_one(new_user)
        flash("Registration successful!", "success")

        # Log the user in by adding their email to the session
        session["user"] = email

        return redirect(url_for("profile", username=email))

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


def generate_random_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(characters) for i in range(length))



@app.route("/admin/reset_password", methods=["POST"])
def reset_password_admin():
    if "user" in session and mongo.db.users.find_one({"email": session["user"], "role": "admin"}):
        user_id = request.form.get("user_id")
        new_password = generate_random_password()  # Генерация случайного пароля

        hashed_password = generate_password_hash(new_password)

        user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
        if user:
            mongo.db.users.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": {"password": hashed_password}}
            )
            flash(f"Password reset successfully for {user['name']}! New password: {new_password}", "success")
        else:
            doctor = mongo.db.doctors.find_one({"_id": ObjectId(user_id)})
            if doctor:
                mongo.db.doctors.update_one(
                    {"_id": ObjectId(user_id)},
                    {"$set": {"password": hashed_password}}
                )
                flash(f"Password reset successfully for Dr. {doctor['name']}! New password: {new_password}", "success")
            else:
                flash("User not found.", "danger")
        return redirect(url_for("admin_users"))
    else:
        flash("You do not have permission to access this page.", "danger")
        return redirect(url_for("index"))
    


@app.route("/admin/delete_user", methods=["POST"])
def delete_user():
    if "user" in session and mongo.db.users.find_one({"email": session["user"], "role": "admin"}):
        user_id = request.form.get("user_id")

        user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
        if user:
            mongo.db.users.delete_one({"_id": ObjectId(user_id)})
            flash("User deleted successfully!", "success")
        else:
            doctor = mongo.db.doctors.find_one({"_id": ObjectId(user_id)})
            if doctor:
                mongo.db.doctors.delete_one({"_id": ObjectId(user_id)})
                flash("User deleted successfully!", "success")
            else:
                flash("User not found.", "danger")
        return redirect(url_for("admin_users"))
    else:
        flash("You do not have permission to access this page.", "danger")
        return redirect(url_for("index"))

@app.route("/change_password", methods=["POST"])
def change_password():
    if "user" in session:
        # Get form data
        user_id = request.form.get("user_id")
        current_password = request.form.get("current_password")
        new_password = request.form.get("new_password")
        confirm_new_password = request.form.get("confirm_new_password")

        # Find the user in the database
        user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
        if not user:
            flash("User not found.", "danger")
            return redirect(url_for("profile", username=session["user"]))

        # Check if the current password is correct
        if not check_password_hash(user["password"], current_password):
            flash("Current password is incorrect.", "danger")
            return redirect(url_for("profile", username=session["user"]))

        # Check if new passwords match
        if new_password != confirm_new_password:
            flash("New passwords do not match.", "danger")
            return redirect(url_for("profile", username=session["user"]))

        # Validate new password requirements
        if not re.match(r"(?=.*\d)(?=.*[A-Z]).{8,}", new_password):
            flash("Password must contain at least 8 characters, including UPPER/lowercase and numbers.", "danger")
            return redirect(url_for("profile", username=session["user"]))

        # Hash the new password
        hashed_password = generate_password_hash(new_password)

        # Update the user's password in the database
        mongo.db.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"password": hashed_password}}
        )

        flash("Password updated successfully!", "success")
        return redirect(url_for("profile", username=session["user"]))
    else:
        flash("You need to log in to change your password.", "danger")
        return redirect(url_for("login"))


@app.route("/request_appointment", methods=["POST"])
def request_appointment():
    if "user" in session:
        # Get form data
        patient_id = request.form.get("patient_id")
        reason = request.form.get("reason")

        # Create a new appointment request
        new_appointment = {
            "patient_id": ObjectId(patient_id),
            "reason": reason,
            "status": "pending",  # Status of the appointment
            "assigned_doctor_id": None,
            "date_requested": datetime.now(timezone.utc)  # Use timezone-aware datetime
        }

        # Insert the new appointment request into the database
        mongo.db.appointments.insert_one(new_appointment)
        flash("Appointment request submitted successfully!", "success")
        return redirect(url_for("profile", username=session["user"]))
    else:
        flash("You need to log in to request an appointment.", "danger")
        return redirect(url_for("login"))


@app.route("/assign_appointment", methods=["POST"])
def assign_appointment():
    if "user" in session and mongo.db.users.find_one({"email": session["user"], "role": "admin"}):
        appointment_id = request.form.get("appointment_id")
        doctor_id = request.form.get("doctor_id")

        # Назначьте врача на встречу
        mongo.db.appointments.update_one(
            {"_id": ObjectId(appointment_id)},
            {"$set": {"assigned_doctor_id": ObjectId(doctor_id), "status": "assigned"}}
        )

        flash("Appointment assigned successfully!", "success")
        return redirect(url_for("profile", username=session["user"]))
    else:
        flash("You do not have permission to assign appointments.", "danger")
        return redirect(url_for("index"))
    
@app.route("/accept_appointment", methods=["POST"])
def accept_appointment():
    if "user" in session:
        current_user = mongo.db.users.find_one({"email": session["user"]}) or mongo.db.doctors.find_one({"email": session["user"]})
        if current_user and (current_user["role"] == "doctor" or current_user["role"] == "admin"):
            appointment_id = request.form.get("appointment_id")
            appointment_date = request.form.get("appointment_date")
            appointment_time = request.form.get("appointment_time")

            appointment_datetime = datetime.strptime(f"{appointment_date} {appointment_time}", "%Y-%m-%d %H:%M")

            doctor_name = current_user.get("name")
            doctor_email = current_user.get("email")

            mongo.db.appointments.update_one(
                {"_id": ObjectId(appointment_id)},
                {"$set": {"status": "scheduled", "appointment_datetime": appointment_datetime,
                    "doctor_name": doctor_name,
                    "doctor_email": doctor_email}}
            )

            flash("Appointment accepted and scheduled successfully!", "success")
            return redirect(url_for("profile", username=session["user"]))
        else:
            flash("You do not have permission to perform this action.", "danger")
            return redirect(url_for("index"))
    else:
        flash("You need to log in to accept appointments.", "danger")
        return redirect(url_for("login"))
    

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
    try:
        # Найти пользователя по email
        user = mongo.db.users.find_one({"email": username})
        if user:
            print(f"User found in users collection: {user}")
        else:
            user = mongo.db.doctors.find_one({"email": username})
            if user:
                print(f"User found in doctors collection: {user}")
            else:
                flash("User not found", "danger")
                return redirect(url_for("index"))

        if user:
            # Текущий пользователь
            current_email = session.get("user")
            current_user = mongo.db.users.find_one({"email": current_email})
            if not current_user:
                current_user = mongo.db.doctors.find_one({"email": current_email})
            if not current_user:
                flash("Current user not found.", "danger")
                return redirect(url_for("index"))
            else:
                print(f"Current user email from session: {current_email}")

            viewing_as_admin = current_user["role"] == "admin" and current_email != username

            # Медицинские записи пользователя
            medical_records = list(mongo.db.medical_records.find({"patient_id": user["_id"]}))
            for record in medical_records:
                doctor = mongo.db.doctors.find_one({"_id": record["doctor_id"]})
                if doctor:
                    record["doctor_name"] = doctor["name"]
                    record["doctor_email"] = doctor["email"]
                patient = mongo.db.users.find_one({"_id": record["patient_id"]})
                if patient:
                    record["patient_name"] = patient["name"]
                    record["patient_email"] = patient["email"]

            # Медицинские записи доктора
            doctor_records = []
            if user["role"] == "doctor":
                doctor_records = list(mongo.db.medical_records.find({"doctor_id": user["_id"]}))
                for record in doctor_records:
                    patient = mongo.db.users.find_one({"_id": record["patient_id"]})
                    if patient:
                        record["patient_name"] = patient["name"]
                        record["patient_email"] = patient["email"]
            else:
                doctor_records = []

            # Назначенные приёмы
            appointments = list(mongo.db.appointments.find({"patient_id": user["_id"]}))
            for appointment in appointments:
                if appointment.get("assigned_doctor_id"):
                    doctor = mongo.db.doctors.find_one({"_id": appointment["assigned_doctor_id"]})
                    if doctor:
                        appointment["doctor_name"] = doctor["name"]
                        appointment["doctor_email"] = doctor["email"]

            # Запросы на приём для администратора
            appointment_requests = []
            if current_user["role"] == "admin":
                appointment_requests = list(mongo.db.appointments.find({"status": "pending"}))

            # Назначенные пациенты для доктора или администратора
            assigned_patients = []
            if user["role"] == "doctor" or current_user["role"] == "admin":
                assigned_patients = list(mongo.db.appointments.find({"assigned_doctor_id": user["_id"]}))
                for appointment in assigned_patients:
                    patient = mongo.db.users.find_one({"_id": appointment["patient_id"]})
                    if patient:
                        appointment["patient_name"] = patient["name"]
                        appointment["patient_email"] = patient["email"]
                        appointment["medical_records"] = list(mongo.db.medical_records.find({"patient_id": patient["_id"]}))
                        print(f"Assigned patient: {appointment}")
                    else:
                        print(f"Patient not found for appointment {appointment['_id']}")

            # Список пациентов для выбора доктором
            patients = list(mongo.db.users.find({"role": "patient"}))
            doctors = list(mongo.db.doctors.find())
            return render_template(
                "profile.html",
                user=user,
                medical_records=medical_records,
                appointments=appointments,
                user_files=list(mongo.db.user_files.find({"user_id": user["_id"]})),
                role=current_user["role"] if viewing_as_admin else user["role"],
                viewing_as_admin=viewing_as_admin,
                appointment_requests=appointment_requests,
                assigned_patients=assigned_patients,
                doctors=doctors,
                patients=patients,
                doctor_records=doctor_records
            )
        else:
            flash("User not found", "danger")
            return redirect(url_for("index"))
    except Exception as e:
        flash(str(e), "danger")
        return redirect(url_for("index"))
    
    

@app.route('/edit_medical_record/<record_id>', methods=['GET', 'POST'])
def edit_medical_record(record_id):
    record = mongo.db.medical_records.find_one({"_id": ObjectId(record_id)})
    if record:
        doctor = mongo.db.doctors.find_one({"_id": record["doctor_id"]})
        patient = mongo.db.users.find_one({"_id": record["patient_id"]})
        files = list(mongo.db.medical_record_files.find({"record_id": ObjectId(record_id)}))
        return render_template("medical_record_detail.html", record=record, doctor=doctor, patient=patient, files=files)
    else:
        flash("Medical record not found.", "danger")
        return redirect(url_for("index"))
    

@app.route('/update_medical_record/<record_id>', methods=['POST'])
def update_medical_record(record_id):
    try:
        description = request.form['description']
        treatment = request.form['treatment']
        record_date = request.form['record_date']

        # Обновление записи в базе данных
        mongo.db.medical_records.update_one(
            {"_id": ObjectId(record_id)},
            {"$set": {
                "description": description,
                "treatment": treatment,
                "date": datetime.strptime(record_date, "%Y-%m-%d")
            }}
        )

        # Загрузка документа
        if 'file' in request.files:
            file = request.files['file']
            if file and allowed_file(file.filename):
                result = cloudinary.uploader.upload(file)
                file_url = result['secure_url']
                file_id = result['public_id']
                file_name = secure_filename(file.filename)

                new_file = {
                    "record_id": ObjectId(record_id),
                    "file_id": file_id,
                    "file_url": file_url,
                    "file_name": file_name,
                    "uploaded_at": datetime.utcnow()
                }
                mongo.db.medical_record_files.insert_one(new_file)

        flash('Medical record updated successfully', 'success')
    except Exception as e:
        flash(str(e), 'danger')

    return redirect(url_for('medical_record_detail', record_id=record_id))


@app.route('/upload_medical_record_file/<record_id>', methods=['POST'])
def upload_medical_record_file(record_id):
    try:
        if 'file' in request.files:
            file = request.files['file']
            if file and allowed_file(file.filename):
                result = cloudinary.uploader.upload(file)
                file_url = result['secure_url']
                file_id = result['public_id']
                file_name = secure_filename(file.filename)

                new_file = {
                    "record_id": ObjectId(record_id),
                    "file_id": file_id,
                    "file_url": file_url,
                    "file_name": file_name,
                    "uploaded_at": datetime.utcnow()
                }
                mongo.db.medical_record_files.insert_one(new_file)

                flash('File uploaded successfully', 'success')
            else:
                flash('Invalid file type', 'danger')
        else:
            flash('No file selected', 'danger')
    except Exception as e:
        flash(str(e), 'danger')

    return redirect(url_for('edit_medical_record', record_id=record_id))

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
        # Fetch all users and doctors
        users = list(mongo.db.users.find())
        doctors = list(mongo.db.doctors.find())
        
        # Sort users: admin first, then doctors, then patients
        admins = [user for user in users if user['role'] == 'admin']
        sorted_doctors = sorted(doctors, key=lambda x: x['name'])
        sorted_patients = sorted([user for user in users if user['role'] == 'patient'], key=lambda x: x['name'])

        # Combine sorted lists
        sorted_users = admins + sorted_doctors + sorted_patients

        return render_template("admin_users.html", users=sorted_users)
    else:
        flash("You do not have permission to access this page.", "danger")
        return redirect(url_for("index"))


@app.route('/add_medical_record', methods=['POST'])
def add_medical_record():
    try:
        patient_id = request.form.get('patient_id')
        doctor_email = session.get('user')
        if not doctor_email:
            raise Exception("Doctor email not found in session.")
        
        doctor = mongo.db.doctors.find_one({"email": doctor_email})
        if not doctor:
            raise Exception("Doctor not found in the database.")
        
        doctor_id = doctor["_id"]
        description = request.form.get('description')
        treatment = request.form.get('treatment')
        record_date = request.form.get('record_date')
        patient_email = request.form.get('patient_email')

        # Проверка наличия всех необходимых данных
        if not all([patient_id, doctor_id, description, treatment, record_date, patient_email]):
            raise Exception("Missing required fields.")
        
        # Добавление записи в БД
        mongo.db.medical_records.insert_one({
            'patient_id': ObjectId(patient_id),
            'doctor_id': ObjectId(doctor_id),
            'description': description,
            'treatment': treatment,
            'date': datetime.strptime(record_date, "%Y-%m-%d")
        })

        flash('Medical record added successfully', 'success')
        return redirect(url_for('profile', username=patient_email))
    except Exception as e:
        flash(str(e), 'danger')
        return redirect(url_for('profile', username=session.get('user')))

@app.route("/medical_record/<record_id>")
def medical_record_detail(record_id):
    record = mongo.db.medical_records.find_one({"_id": ObjectId(record_id)})
    if record:
        doctor = mongo.db.doctors.find_one({"_id": record["doctor_id"]})
        patient = mongo.db.users.find_one({"_id": record["patient_id"]})
        return render_template("medical_record_detail.html", record=record, doctor=doctor, patient=patient)
    else:
        flash("Medical record not found.", "danger")
        return redirect(url_for("index"))


if __name__ == "__main__":
    # Run the Flask application
    app.run(
        host=os.environ.get("IP"), port=int(os.environ.get("PORT")), debug=True
    )