import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import certifi
from werkzeug.security import generate_password_hash, check_password_hash

# Checking if env.py file exists for environment variables
if os.path.exists("env.py"):
    import env

# Creating Flask application instance
app = Flask(__name__)

# Configuration for MongoDB connection using environment variables
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

# Initializing PyMongo with Flask application instance with certifi
mongo = PyMongo(app, tlsCAFile=certifi.where())

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
        age = request.form.get("age")
        phone = request.form.get("phone")
        email = request.form.get("email").lower()  # Convert email to lower case
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        
        # Check if the email already exists
        existing_user = mongo.db.users.find_one({"email": email})
        if existing_user:
            flash("Email already exists. Please use a different email.", "danger")
            return redirect(url_for("signup"))

        # Check if passwords match
        if password == confirm_password:
            # Hash the password
            hashed_password = generate_password_hash(password)
            # Create a new user record
            new_user = {
                "name": name,
                "gender": gender,
                "age": age,
                "phone": phone,
                "email": email,
                "password": hashed_password
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
        email = request.form.get("email").lower()  # Convert email to lower case
        password = request.form.get("password")
        
        # Find the user by email
        existing_user = mongo.db.users.find_one({"email": email})

        if existing_user:
            # Check if the password matches
            if check_password_hash(existing_user["password"], password):
                session["user"] = email
                flash("Welcome, {}".format(existing_user["name"]), "success")
                return redirect(url_for("profile", username=email))
            else:
                flash("Incorrect Email and/or Password", 'danger')
                return redirect(url_for("login"))

        else:
            flash("Incorrect Email and/or Password", 'danger')
            return redirect(url_for("login"))

    # Render the login template
    return render_template("login.html")

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

@app.route("/profile/<username>")
def profile(username):
    # Find the user by email
    user = mongo.db.users.find_one({"email": username})
    if user:
        # Get user's medical records
        medical_records = list(mongo.db.medical_records.find({"patient_id": user["_id"]}))
        
        # Get user's appointments
        appointments = list(mongo.db.appointments.find({"patient_id": user["_id"]}))
        
        # Render the profile template with user data
        return render_template("profile.html", user=user, medical_records=medical_records, appointments=appointments)
    else:
        # This case should not occur if login logic is correct, but it's a good safety measure
        flash("User not found", "danger")
        return redirect(url_for("index"))

if __name__ == "__main__":
    # Run the Flask application
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)