# Import necessary modules and packages for the Flask application
import os
from flask import (
    Flask, flash, render_template, jsonify,
    redirect, request, session, url_for, abort
)
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


# Render the 'index.html' template to display the main page
@app.route("/")
def index():
    """Render the main index page."""
    return render_template('index.html')


# Route to handle user signup
@app.route("/signup", methods=["GET", "POST"])
def signup():
    """
    Handle user signup by processing form data, validating inputs,
    and saving a new user to the database.
    """
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
            # If email exists, show error message and redirect to signup page
            flash(
                "Email already exists. Please use a different email.", "danger"
            )
            return redirect(url_for("signup"))

        # Check if passwords match
        if password != confirm_password:
            # If passwords do not match, show an error message
            # and redirect to signup page
            flash("Passwords do not match. Please try again.", "danger")
            return redirect(url_for("signup"))

        # Validate password requirements
        if not re.match(r"(?=.*\d)(?=.*[A-Z]).{8,}", password):
            flash(
                "Must contain at least 8 char., including UPPERcase & number",
                "danger"
            )
            return redirect(url_for("signup"))

        # Validate date of birth
        try:
            dob_date = datetime.strptime(dob, '%Y-%m-%d')
            current_date = datetime.now()
            # 18 years ago
            min_date = current_date - timedelta(days=6570)
            # 100 years ago
            max_date = current_date - timedelta(days=36525)

            if dob_date < max_date or dob_date > min_date:
                flash(
                    "Date of Birth must be between 18 and 100 years ago.",
                    "danger"
                )
                return redirect(url_for("signup"))
        except ValueError:
            flash("Invalid Date of Birth format.", "danger")
            return redirect(url_for("signup"))

        # Hash the password
        hashed_password = generate_password_hash(password)
        # Create a new user record to be inserted into the database
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

    # Calculate date range for date of birth
    current_date = datetime.now()
    # 18 years ago
    max_date = (current_date - timedelta(days=6570)).strftime('%Y-%m-%d')
    # 100 years ago
    min_date = (current_date - timedelta(days=36525)).strftime('%Y-%m-%d')

    # Render the signup template
    return render_template("signup.html", max_date=max_date, min_date=min_date)
    # Render the signup template
    # return render_template("signup.html")


# Route to handle user login
@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Handle user login by validating form data, checking credentials,
    and establishing a user session.
    """
    if request.method == "POST":
        # Get form data from the login form
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
                # If password matches, set the session for the user
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
                # If password does not match, show an error message
                flash("Incorrect Email and/or Password", 'danger')
                return redirect(url_for("login"))

        else:
            # If user is not found, show an error message
            flash("Incorrect Email and/or Password", 'danger')
            return redirect(url_for("login"))
    # Render the login template
    return render_template("login.html")


# Function to generate an image name
def generate_image_name(full_name):
    """
    Generate an image name by converting the full name to lowercase
    and replacing spaces with hyphens.

    Parameters:
    full_name (str): The full name to be converted.

    Returns:
    str: The generated image name.
    """
    return full_name.lower().replace(" ", "-")


# Route to handle adding a new doctor by admin
@app.route("/add_doctor", methods=["GET", "POST"])
def add_doctor():
    """
    Handle the addition of a new doctor by processing form data,
    validating inputs, and saving the new doctor to the database.
    Only accessible by an admin user.
    """
    if "user" in session and mongo.db.users.find_one(
        {"email": session["user"], "role": "admin"}
    ):
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

        # Render the add doctor template
        return render_template("add_doctor.html")
    else:
        abort(403)


def generate_random_password(length=12):
    """
    Generate a random password with the specified length.

    The password includes a mix of uppercase and lowercase letters,
    digits, and punctuation characters to ensure strong security.

    Args:
        length (int): The length of the generated password. Default is 12.

    Returns:
        str: A randomly generated password.
    """
    # Define the characters to be used in the password
    characters = string.ascii_letters + string.digits + string.punctuation
    # Generate the password using a secure random choice of characters
    return ''.join(secrets.choice(characters) for i in range(length))


# Route for admin to reset user passwords
@app.route("/admin/reset_password", methods=["POST"])
def reset_password_admin():
    """
    Route to allow an admin to reset a user's password.

    If the logged-in user is an admin, generate a new random password,
    hash it, and update the password in the database for the specified user.

    The new password is displayed to the admin for further communication
    to the user. If the user is not found, corresponding message is displayed.
    """
    if "user" in session and mongo.db.users.find_one(
        {"email": session["user"], "role": "admin"}
    ):
        # Get the user ID from the form
        user_id = request.form.get("user_id")
        # Generate a new random password
        new_password = generate_random_password()
        # Hash the new password
        hashed_password = generate_password_hash(new_password)

        # Check if the user exists in the users collection
        user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
        if user:
            # Update the password in the users collection
            mongo.db.users.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": {"password": hashed_password}}
            )
            # Flash a success message with the new password
            flash(
                f"Password reset successfully for {user['name']}! "
                f"New password: {new_password}", "success"
            )
        else:
            # If user not found in users, check in doctors collection
            doctor = mongo.db.doctors.find_one({"_id": ObjectId(user_id)})
            if doctor:
                # Update the password in the doctors collection
                mongo.db.doctors.update_one(
                    {"_id": ObjectId(user_id)},
                    {"$set": {"password": hashed_password}}
                )
                # Flash a success message with the new password
                flash(
                    f"Password reset successfully for Dr. {doctor['name']}! "
                    f"New password: {new_password}", "success"
                )
            else:
                # Flash a danger message if the user is not found
                flash("User not found.", "danger")
        return redirect(url_for("admin_users"))
    else:
        # Flash a danger message if the user is not an admin
        flash("You do not have permission to access this page.", "danger")
        return redirect(url_for("index"))


# Route for admin to delete a user or doctor
@app.route("/admin/delete_user", methods=["POST"])
def delete_user():
    """
    Route to allow an admin to delete a user or doctor.

    If the logged-in user is an admin, delete the user or doctor
    specified by the user_id from the database.
    """
    if "user" in session and mongo.db.users.find_one(
       {"email": session["user"], "role": "admin"}
    ):
        # Get the user ID from the form
        user_id = request.form.get("user_id")

        # Check if the user exists in the users collection
        user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
        if user:
            # Delete the user from the users collection
            mongo.db.users.delete_one({"_id": ObjectId(user_id)})
            flash("User deleted successfully!", "success")
        else:
            # If user not found in users, check in doctors collection
            doctor = mongo.db.doctors.find_one({"_id": ObjectId(user_id)})
            if doctor:
                # Delete the doctor from the doctors collection
                mongo.db.doctors.delete_one({"_id": ObjectId(user_id)})
                flash("User deleted successfully!", "success")
            else:
                # Flash a danger message if the user is not found
                flash("User not found.", "danger")
        return redirect(url_for("admin_users"))
    else:
        # Flash a danger message if the user is not an admin
        flash("You do not have permission to access this page.", "danger")
        return redirect(url_for("index"))


# Route for user to change their password
@app.route("/change_password", methods=["POST"])
def change_password():
    """
    Route to allow a logged-in user to change their password.

    The user must provide their current password and the new password twice.
    The new password must meet the specified requirements.

    Displays appropriate messages for success or failure scenarios.
    """
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
            flash(
                "Password must contain at least 8 characters, "
                "including UPPERcase and numbers.", "danger"
            )
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


# Route for users to request an appointment
@app.route("/request_appointment", methods=["POST"])
def request_appointment():
    """
    Route to handle appointment requests from logged-in users.

    The user must provide their patient ID and the reason for the appointment.
    Appointment request is then stored in DB with a pending status.

    Displays appropriate messages for success or failure scenarios.
    """
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
            "date_requested": datetime.now(timezone.utc)
        }

        # Insert the new appointment request into the database
        mongo.db.appointments.insert_one(new_appointment)
        flash("Appointment request submitted successfully!", "success")
        return redirect(url_for("profile", username=session["user"]))
    else:
        flash("You need to log in to request an appointment.", "danger")
        return redirect(url_for("login"))


# Route to assign a doctor to an appointment
@app.route("/assign_appointment", methods=["POST"])
def assign_appointment():
    """
    Route to assign a doctor to an appointment by an admin user.

    The admin must provide the appointment ID and doctor ID.
    The appointment's status is updated to 'assigned' and doctor is assigned.

    Displays appropriate messages for success or failure scenarios.
    """
    if "user" in session and mongo.db.users.find_one(
        {"email": session["user"], "role": "admin"}
    ):
        # Get form data
        appointment_id = request.form.get("appointment_id")
        doctor_id = request.form.get("doctor_id")

        # Assign the doctor to the appointment
        mongo.db.appointments.update_one(
            {"_id": ObjectId(appointment_id)},
            {
                "$set": {
                    "assigned_doctor_id": ObjectId(doctor_id),
                    "status": "assigned"
                }
            }
        )

        flash("Appointment assigned successfully!", "success")
        return redirect(url_for("profile", username=session["user"]))
    else:
        flash("You do not have permission to assign appointments.", "danger")
        return redirect(url_for("index"))


# Route to accept and schedule an appointment by a doctor or admin
@app.route("/accept_appointment", methods=["POST"])
def accept_appointment():
    """
    Allows doctors or admins to accept and schedule an appointment.

    The function updates the appointment status to 'scheduled',
    sets the appointment datetime, and records the doctor's name and email.

    Displays appropriate messages for success or failure scenarios.
    """
    if "user" in session:
        # Find the current user in the users or doctors collection
        current_user = mongo.db.users.find_one(
            {"email": session["user"]}
        ) or mongo.db.doctors.find_one(
            {"email": session["user"]}
        )
        # Check if the current user is a doctor or admin
        if current_user and (
            current_user["role"] == "doctor" or current_user["role"] == "admin"
        ):
            # Get form data
            appointment_id = request.form.get("appointment_id")
            appointment_date = request.form.get("appointment_date")
            appointment_time = request.form.get("appointment_time")

            # Combine date and time into a single datetime object
            appointment_datetime = datetime.strptime(
                f"{appointment_date} {appointment_time}", "%Y-%m-%d %H:%M"
            )

            # Get doctor's name and email
            doctor_name = current_user.get("name")
            doctor_email = current_user.get("email")

            # Update the appointment in the database
            mongo.db.appointments.update_one(
                {"_id": ObjectId(appointment_id)},
                {
                    "$set": {
                        "status": "scheduled",
                        "appointment_datetime": appointment_datetime,
                        "doctor_name": doctor_name,
                        "doctor_email": doctor_email
                    }
                }
            )

            flash(
                "Appointment accepted and scheduled successfully!", "success"
            )
            return redirect(url_for("profile", username=session["user"]))
        else:
            flash(
                "You do not have permission to perform this action.", "danger"
            )
            return redirect(url_for("index"))
    else:
        flash("You need to log in to accept appointments.", "danger")
        return redirect(url_for("login"))


# Route to handle user logout
@app.route("/logout")
def logout():
    """
    Logs out the user by removing their session and redirects to index page.

    The function also ensures the response is not cached by setting appropriate
    HTTP headers.
    """
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


# Route to display the list of doctors
@app.route("/doctors")
def doctors():
    """
    Fetches the list of doctors from DB
    and renders the doctors template.
    """
    doctors_list = mongo.db.doctors.find()
    return render_template("doctors.html", doctors=doctors_list)


# Context processor to provide utility functions to all templates
@app.context_processor
def utility_processor():
    """Adds utility functions to the Jinja2 context for all templates."""
    def get_image_path(image_name):
        """
        Constructs the image path for a doctor based on their image name.

        Args:
            image_name (str): The name of the doctor's image file.

        Returns:
            str: The full path to the doctor's image.
        """
        image_path = f'images/doctors/{image_name}-600.webp'
        if image_name:
            return image_path
        else:
            return 'images/doctors/default-doctor.webp'

    return dict(get_image_path=get_image_path)


# Route to display the privacy policy page
@app.route("/policy")
def policy():
    """Renders the privacy policy template."""
    return render_template("policy.html")


# Route to display the about page
@app.route("/about")
def about():
    """Renders the about template."""
    return render_template("about.html")


# Route to display the user's profile
@app.route("/profile/<username>")
def profile(username):
    """
    Route to display the user's profile, including medical records,
    appointments, and user-specific data. It handles data retrieval for both
    patients and doctors and provides necessary information for admin users.

    Args:
        username (str): The email of the user whose profile is to be displayed.

    Returns:
        str: Rendered HTML template for the user's profile.
    """
    try:
        # Find the user by email in the users collection
        user = mongo.db.users.find_one({"email": username})
        # If not found, check in the doctors collection
        if not user:
            user = mongo.db.doctors.find_one({"email": username})
            if not user:
                flash("User not found", "danger")
                return redirect(url_for("index"))

        if user:
            # Get the current user's email from the session
            current_email = session.get("user")
            current_user = mongo.db.users.find_one({"email": current_email})
            if not current_user:
                current_user = mongo.db.doctors.find_one(
                    {"email": current_email}
                )
            if not current_user:
                abort(403)

            # Determine if the current user is an admin viewing another profile
            viewing_as_admin = (
                current_user["role"] == "admin" and current_email != username
            )

            # Retrieve the user's medical records
            medical_records = list(
                mongo.db.medical_records.find({"patient_id": user["_id"]})
            )
            for record in medical_records:
                doctor = mongo.db.doctors.find_one(
                    {"_id": record["doctor_id"]}
                )
                if doctor:
                    record["doctor_name"] = doctor["name"]
                    record["doctor_email"] = doctor["email"]
                patient = mongo.db.users.find_one(
                    {"_id": record["patient_id"]}
                )
                if patient:
                    record["patient_name"] = patient["name"]
                    record["patient_email"] = patient["email"]

            # Retrieve medical records for doctors
            doctor_records = []
            if user["role"] == "doctor":
                doctor_records = list(
                    mongo.db.medical_records.find({"doctor_id": user["_id"]})
                )
                for record in doctor_records:
                    patient = mongo.db.users.find_one(
                        {"_id": record["patient_id"]}
                    )
                    if patient:
                        record["patient_name"] = patient["name"]
                        record["patient_email"] = patient["email"]
            else:
                doctor_records = []

            # Retrieve the user's appointments
            appointments = list(
                mongo.db.appointments.find({"patient_id": user["_id"]})
            )
            for appointment in appointments:
                if appointment.get("assigned_doctor_id"):
                    doctor = mongo.db.doctors.find_one(
                        {"_id": appointment["assigned_doctor_id"]}
                    )
                    if doctor:
                        appointment["doctor_name"] = doctor["name"]
                        appointment["doctor_email"] = doctor["email"]

            # Retrieve pending appointment requests for admin users
            appointment_requests = []
            if current_user["role"] == "admin":
                appointment_requests = list(
                    mongo.db.appointments.find({"status": "pending"})
                )
                for appointment in appointment_requests:
                    patient = mongo.db.users.find_one(
                        {"_id": appointment["patient_id"]}
                    )
                    if patient:
                        appointment["patient_name"] = patient["name"]
                        appointment["patient_email"] = patient["email"]

            # Retrieve pending appointment requests for patients
            patient_requests = []
            if user["role"] == "patient":
                patient_requests = list(
                    mongo.db.appointments.find(
                        {"patient_id": user["_id"], "status": "pending"}
                    )
                )

            # Retrieve assigned patients for doctors or admin users
            assigned_patients = []
            if user["role"] == "doctor" or current_user["role"] == "admin":
                assigned_patients = list(mongo.db.appointments.find(
                    {"assigned_doctor_id": user["_id"]})
                )
                for appointment in assigned_patients:
                    patient = mongo.db.users.find_one(
                        {"_id": appointment["patient_id"]}
                    )
                    if patient:
                        appointment["patient_name"] = patient["name"]
                        appointment["patient_email"] = patient["email"]
                        appointment["medical_records"] = list(
                            mongo.db.medical_records.find(
                                {"patient_id": patient["_id"]}
                            )
                        )

            # Retrieve the list of patients for doctor selection
            patients = list(mongo.db.users.find({"role": "patient"}))
            doctors = list(mongo.db.doctors.find())
            return render_template(
                "profile.html",
                user=user,
                medical_records=medical_records,
                appointments=appointments,
                user_files=list(
                    mongo.db.user_files.find({"user_id": user["_id"]})
                ),
                role=(
                    current_user["role"] if viewing_as_admin else user["role"]
                ),
                viewing_as_admin=viewing_as_admin,
                appointment_requests=appointment_requests,
                assigned_patients=assigned_patients,
                doctors=doctors,
                patients=patients,
                doctor_records=doctor_records,
                patient_requests=patient_requests
            )
        else:
            flash("User not found", "danger")
            return redirect(url_for("index"))
    except Exception as e:
        flash(str(e), "danger")
        return redirect(url_for("index"))


# Route to display and edit a specific medical record
@app.route('/edit_medical_record/<record_id>', methods=['GET', 'POST'])
def edit_medical_record(record_id):
    """
    Route to display and edit a specific medical record. Fetches the record,
    associated doctor, patient, and related files. Renders the detail view
    with the capability for admins to edit the record.

    Args:
        record_id (str): The ID of the medical record to be edited.

    Returns:
        str: Rendered HTML template for the medical record detail.
    """
    # Get current user's email from session
    current_email = session.get("user")
    # Find the current user in the users or doctors collection
    current_user = mongo.db.users.find_one(
        {"email": current_email}
    ) or mongo.db.doctors.find_one(
        {"email": current_email}
    )

    # If no user is found or user is not a doctor/admin, return 403 error
    if not current_user or current_user["role"] not in ["doctor", "admin"]:
        abort(403)

    # Find the medical record in the database
    record = mongo.db.medical_records.find_one({"_id": ObjectId(record_id)})
    if record:
        # Fetch associated doctor and patient information
        doctor = mongo.db.doctors.find_one({"_id": record["doctor_id"]})
        patient = mongo.db.users.find_one({"_id": record["patient_id"]})
        # Fetch files related to the medical record
        files = list(
            mongo.db.medical_record_files.find(
                {"record_id": ObjectId(record_id)}
            )
        )
        # Get current user's email from session
        current_email = session.get("user")
        # Find the current user in the users or doctors collection
        current_user = mongo.db.users.find_one(
            {"email": current_email}
        ) or mongo.db.doctors.find_one(
            {"email": current_email}
        )
        if not current_user:
            abort(403)

        # Format the record date
        record_date = record["date"].strftime("%Y-%m-%d")

        # Check if the current user is viewing as an admin
        viewing_as_admin = current_user.get("role") == "admin"

        # Render the medical record detail template
        return render_template(
            "medical_record_detail.html",
            record=record,
            doctor=doctor,
            patient=patient,
            current_user=current_user,
            viewing_as_admin=viewing_as_admin,
            files=files,
            record_date=record_date
        )
    else:
        flash("Medical record not found.", "danger")
        return redirect(url_for("index"))


# Route to update a specific medical record
@app.route('/update_medical_record/<record_id>', methods=['POST'])
def update_medical_record(record_id):
    """
    Updates the medical record with the given record_id. The function updates
    the description, treatment, and date of the medical record in the database.
    If a file is uploaded, it is uploaded to Cloudinary, and the file details
    are saved in the medical_record_files collection.

    Args:
        record_id (str): The ID of the medical record to be updated.

    Returns:
        redirect: Redirects to the medical record detail page.
    """
    try:
        current_email = session.get("user")
        current_user = mongo.db.users.find_one(
            {"email": current_email}
        ) or mongo.db.doctors.find_one({"email": current_email})
        if not current_user or current_user["role"] not in ["doctor", "admin"]:
            abort(403)

        # Retrieve form data
        description = request.form['description']
        treatment = request.form['treatment']
        record_date = request.form['record_date']

        # Update the record in the database
        mongo.db.medical_records.update_one(
            {"_id": ObjectId(record_id)},
            {"$set": {
                "description": description,
                "treatment": treatment,
                "date": datetime.strptime(record_date, "%Y-%m-%d")
            }}
        )

        # Upload the document
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


# Route to delete an assigned patient, accessible to doctors and admins
@app.route('/api/deletePatient/<patient_id>', methods=['DELETE'])
def delete_patient(patient_id):
    """
    Handle the deletion of a patient from the assigned list.
    This route is accessible to users with roles 'doctor' or 'admin',
    or those viewing as admin.
    """
    # Check if the user is logged in
    if "user" in session:
        # Get the current user's email from the session
        current_email = session["user"]
        # Find the current user in either users or doctors collections
        current_user = mongo.db.users.find_one(
            {"email": current_email}
        ) or mongo.db.doctors.find_one({"email": current_email})

        # Check if the current user has the appropriate role
        if current_user and current_user["role"] in [
            'doctor', 'admin'
        ] or (
            current_user["role"] == "admin" and session.get("viewing_as_admin")
        ):
            # Find the patient by ID and delete
            patient = mongo.db.appointments.find_one(
                {"_id": ObjectId(patient_id)}
            )
            if patient:
                mongo.db.appointments.delete_one({"_id": ObjectId(patient_id)})
                return jsonify({'success': True})
            else:
                return jsonify(
                    {'success': False, 'message': 'Patient not found'}
                ), 404
        else:
            return jsonify(
                {'success': False, 'message': 'Insufficient permissions'}
            ), 403
    else:
        return jsonify(
            {'success': False, 'message': 'User not authenticated'}
        ), 403


# Route to upload a file to a specific medical record
@app.route('/upload_medical_record_file/<record_id>', methods=['POST'])
def upload_medical_record_file(record_id):
    """
    Uploads a file to the medical record with the given record_id. The function
    checks if a file is provided, verifies the file type, uploads the file to
    Cloudinary, and saves file details in the medical_record_files collection.

    Args:
        record_id (str): The ID of the medical record to upload the file to.

    Returns:
        redirect: Redirects to the edit medical record page.
    """
    try:
        # Check if a file is provided in the request
        if 'file' in request.files:
            file = request.files['file']
            # Validate the file type
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
                # Insert the file details into the database
                mongo.db.medical_record_files.insert_one(new_file)

                flash('File uploaded successfully', 'success')
            else:
                flash('Invalid file type', 'danger')
        else:
            flash('No file selected', 'danger')
    except Exception as e:
        flash(str(e), 'danger')

    return redirect(url_for('edit_medical_record', record_id=record_id))


# Route to handle AJAX requests for editing user information
@app.route("/edit_user_ajax", methods=["POST"])
def edit_user_ajax():
    """
    Handles AJAX requests for editing user information. This function checks
    the current session, verifies the user's identity and permissions,
    updates the user information in the database, and returns a JSON response
    indicating success or failure.

    Returns:
        dict: JSON response containing success status, message,
        and optional redirect URL.
    """
    if "user" in session:
        current_email = session["user"]
        current_user = mongo.db.users.find_one(
            {"email": current_email}
        ) or mongo.db.doctors.find_one(
            {"email": current_email}
        )
        if current_user:
            user_id = request.json.get("user_id")
            user = mongo.db.users.find_one(
                {"_id": ObjectId(user_id)}
            ) or mongo.db.doctors.find_one(
                {"_id": ObjectId(user_id)}
            )

            if user:
                if current_user["role"] != "admin":
                    current_password = request.json.get("current_password")

                    # Verify current password
                    if not check_password_hash(
                        user["password"], current_password
                    ):
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

                # Update session email if admin is editing their own profile
                # and email changed
                if (
                    current_user["_id"] == user["_id"]
                    and current_email != new_email
                ):
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
                return {"success": False, "message": "User not found."}, 404
        else:
            return (
                {"success": False, "message": "Current user not found."}, 404
            )
    else:
        return {
            "success": False,
            "message": "You need to log in to edit user information."
        }, 403


# Route to handle AJAX file uploads
@app.route("/upload_file_ajax", methods=["POST"])
def upload_file_ajax():
    """
    Handles AJAX requests for uploading files.
    This function checks the current session,
    validates the uploaded file, uploads it to Cloudinary,
    saves the file information in the database,
    and returns a JSON response indicating success or failure.

    Returns:
        dict: JSON response containing success status,
        message, and optional file information.
    """
    if "user" in session:
        # Retrieve the uploaded file and form data
        file = request.files.get("file")
        file_type = request.form.get("file_type")
        user_id = request.form.get("user_id")

        # Check if the file is allowed and present
        if file and allowed_file(file.filename):
            # Upload the file to Cloudinary
            result = cloudinary.uploader.upload(file)

            # Extract file details from the upload result
            file_url = result['secure_url']
            file_id = result['public_id']
            file_name = secure_filename(file.filename)

            # Create a new file record to save in the database
            new_file = {
                "user_id": ObjectId(user_id),
                "file_id": file_id,
                "file_url": file_url,
                "file_name": file_name,
                "file_type": file_type,
                "uploaded_at": datetime.utcnow()
            }
            mongo.db.user_files.insert_one(new_file)

            # Return success response with file information
            return jsonify({
                "success": True,
                "message": "File uploaded successfully.",
                "file_id": file_id,
                "file_url": file_url,
                "file_name": file_name
            })
        else:
            # Return error response for invalid file type
            return jsonify({
                "success": False,
                "message": "Invalid file type."
            }), 400
    else:
        # Return error response if the user is not logged in
        return jsonify({
            "success": False,
            "message": "You need to log in to upload files."
        }), 403


# Route to handle file deletion
@app.route("/delete_file", methods=["POST"])
def delete_file():
    """
    Handles requests to delete a file.
    This function checks the current session,
    attempts to delete the file from Cloudinary,
    removes the file record from the database,
    and returns a JSON response indicating success or failure.

    Returns:
        dict: JSON response containing success status and message.
    """
    if "user" in session:
        # Get the file ID from the form data
        file_id = request.form.get("file_id")
        if file_id:
            # Attempt to delete the file from Cloudinary
            if delete_from_cloudinary(file_id):
                # Find the file record in the database
                file_record = mongo.db.user_files.find_one(
                    {"file_id": file_id}
                )
                if file_record:
                    # Delete the file record from the database
                    result = mongo.db.user_files.delete_one(
                        {"file_id": file_id}
                    )
                    if result.deleted_count > 0:
                        # Return success response
                        return jsonify(
                            {
                                "success": True,
                                "message": "File deleted successfully."
                            }
                        )
                    else:
                        # Return error response if the file was not found in DB
                        return jsonify(
                            {
                                "success": False,
                                "message": (
                                    "File deleted from Cloudinary but not "
                                    "found in the database."
                                )
                            }
                        )
                else:
                    # Return error response if the file record was not found
                    return jsonify(
                        {
                            "success": False,
                            "message": "File not found in the database."
                        }
                    )
            else:
                # Return error response if file deletion from Cloudinary failed
                return jsonify(
                    {
                        "success": False,
                        "message": "Failed to delete the file from Cloudinary."
                    }
                )
        else:
            # Return error response if the file ID is not provided
            return jsonify(
                {
                    "success": False,
                    "message": "File ID is required."
                }
            )
    else:
        # Return error response if the user is not logged in
        return jsonify(
            {
                "success": False,
                "message": "You need to log in to delete files."
            }
        )


# Function to delete a file from Cloudinary
def delete_from_cloudinary(file_id):
    """
    Deletes a file from Cloudinary using its file ID.

    Args:
        file_id (str): The ID of the file to be deleted from Cloudinary.

    Returns:
        bool: True if the file was deleted successfully, False otherwise.
    """
    try:
        # Attempt to delete the file from Cloudinary
        result = cloudinary.uploader.destroy(file_id)
        return result.get("result") == "ok"
    except Exception as error:
        return False


# Function to check if a file has an allowed extension
def allowed_file(filename):
    """
    Checks if the uploaded file has an allowed extension.

    Args:
        filename (str): The name of the file to be checked.

    Returns:
        bool: True if the file extension is allowed, False otherwise.
    """
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "pdf", "doc", "docx"}
    # Check if the file has a valid extension
    return (
        "." in filename and
        filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


# Route to view and manage all users for admin
@app.route("/admin/users")
def admin_users():
    """
    Route to display all users and doctors for the admin.
    Fetches user data from the database, sorts it, and renders
    the admin_users.html template.
    """
    if "user" in session and mongo.db.users.find_one(
        {"email": session["user"], "role": "admin"}
    ):
        # Fetch all users and doctors
        users = list(mongo.db.users.find())
        doctors = list(mongo.db.doctors.find())

        # Sort users: admin first, then doctors, then patients
        admins = [user for user in users if user['role'] == 'admin']
        sorted_doctors = sorted(doctors, key=lambda x: x['name'])
        sorted_patients = sorted(
            [user for user in users if user['role'] == 'patient'],
            key=lambda x: x['name']
        )

        # Combine sorted lists
        sorted_users = admins + sorted_doctors + sorted_patients

        return render_template("admin_users.html", users=sorted_users)
    else:
        flash("You do not have permission to access this page.", "danger")
        return redirect(url_for("index"))


# Route to handle adding a medical record
@app.route('/add_medical_record', methods=['POST'])
def add_medical_record():
    """
    Route to add a new medical record to the database.
    Validates the required fields and saves the record.
    Redirects to the patient's profile page upon success or failure.
    """
    try:
        # Get form data
        patient_id = request.form.get('patient_id')
        doctor_email = session.get('user')
        if not doctor_email:
            raise Exception("Doctor email not found in session.")

        # Find the doctor in the database
        doctor = mongo.db.doctors.find_one({"email": doctor_email})
        if not doctor:
            raise Exception("Doctor not found in the database.")

        doctor_id = doctor["_id"]
        description = request.form.get('description')
        treatment = request.form.get('treatment')
        record_date = request.form.get('record_date')

        # Check for the presence of all required data
        if not all(
            [
                patient_id,
                doctor_id,
                description,
                treatment,
                record_date
            ]
        ):
            raise Exception("Missing required fields.")

        # Add the medical record to the database
        mongo.db.medical_records.insert_one({
            'patient_id': ObjectId(patient_id),
            'doctor_id': ObjectId(doctor_id),
            'description': description,
            'treatment': treatment,
            'date': datetime.strptime(record_date, "%Y-%m-%d")
        })

        flash('Medical record added successfully', 'success')
        return redirect(url_for('profile', username=session.get('user')))
    except Exception as e:
        flash(str(e), 'danger')
        return redirect(url_for('profile', username=session.get('user')))


# Route to view the details of a specific medical record
@app.route("/medical_record/<record_id>")
def medical_record_detail(record_id):
    """
    Route to display the details of a specific medical record.
    Fetches the record, associated doctor, and patient from the database.
    Renders the medical record detail template
    or redirects with an error message if not found.
    """
    # Get current user's email from session
    current_email = session.get("user")
    # Find the current user in the users or doctors collection
    current_user = mongo.db.users.find_one(
        {"email": current_email}
    ) or mongo.db.doctors.find_one({"email": current_email})

    if not current_user:
        abort(403)

    # Find the medical record in the database
    record = mongo.db.medical_records.find_one({"_id": ObjectId(record_id)})
    if record:
        # Find the associated doctor and patient
        doctor = mongo.db.doctors.find_one({"_id": record["doctor_id"]})
        patient = mongo.db.users.find_one({"_id": record["patient_id"]})
        if not current_user:
            abort(403)
        # Render the medical record detail template
        return render_template(
            "medical_record_detail.html",
            record=record,
            doctor=doctor,
            patient=patient,
            current_user=current_user
        )
    else:
        # Flash an error message if the record is not found
        flash("Medical record not found.", "danger")
        return redirect(url_for("index"))


# Error handler for 403 Forbidden
@app.errorhandler(403)
def forbidden(error):
    """
    Error handler for 403 Forbidden.
    Renders the 403.html template when a 403 error occurs.
    """
    return render_template('403.html'), 403


# Error handler for 404 Page Not Found
@app.errorhandler(404)
def page_not_found(error):
    """
    Error handler for 404 Page Not Found.
    Renders the 404.html template when a 404 error occurs.
    """
    return render_template('404.html'), 404


if __name__ == "__main__":
    # Ensure default values for IP
    # and PORT if environment variables are not set
    host = os.environ.get("IP", "0.0.0.0")
    port = int(os.environ.get("PORT", 5000))
    app.run(host=host, port=port, debug=False)
