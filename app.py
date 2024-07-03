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
    return render_template('index.html')


from flask import jsonify

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form.get("name")
        gender = request.form.get("gender")
        age = request.form.get("age")
        phone = request.form.get("phone")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        # Check if user already exists
        existing_user = mongo.db.users.find_one({"email": email})
        if existing_user:
            flash("Email already exists. Please use a different email.")
            return redirect(url_for("signup"))
        
        if password == confirm_password:
            hashed_password = generate_password_hash(password)
            new_user = {
                "name": name,
                "gender": gender,
                "age": age,
                "phone": phone,
                "email": email,
                "password": hashed_password
            }
            mongo.db.users.insert_one(new_user)
            flash("Registration successful! Please check your email to verify your account.")
            # Code to send email notification can be added here
            return redirect(url_for("login"))
        else:
            flash("Passwords do not match. Please try again.")
            return redirect(url_for("signup"))

    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                flash("Welcome, {}".format(
                    request.form.get("username")))
                return redirect(url_for(
                    "profile", username=session["user"]))
            else:
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)