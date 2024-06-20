import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import certifi

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


# Route to check connection to MongoDB
@app.route("/")
def connect_check():
    try:
        # Ping MongoDB to check connection
        mongo.db.command("ping")  
        return "Connection to MongoDB established successfully!"
    except Exception as e:
        return f"Error connecting to MongoDB: {str(e)}"

# Route to get user information
@app.route("/users")    
def get_users():
    try:
        users = mongo.db.users.find()
        user_list = []
        for user in users:
            user_list.append({
                "id": str(user["_id"]),
                "name": user["name"],
                "email": user["email"],
                "phone": user["phone"],
                "role": user["role"],
                "age": user["age"],
                "gender": user["gender"],
                "specialization": user["specialization"],
                "experience_years": user["experience_years"]
            })
        return {"users": user_list}, 200
    except Exception as e:
        return f"Error retrieving users: {str(e)}", 500

if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
    

# Original line
mongo = PyMongo(app)

# Modified line
mongo = PyMongo(app, tlsCAFile=certifi.where())