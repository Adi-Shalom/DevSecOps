import os
from flask import Flask, request, jsonify
from pymongo import MongoClient, errors

app = Flask(__name__)

# MongoDB setup with environment variable for MongoDB URI
mongo_uri = os.getenv('MONGO_URI', 'mongodb://root:example@mongodb:27017/flask_microservices')

try:
    # Try to connect to MongoDB
    client = MongoClient(mongo_uri)
    db = client["flask_microservices"]
    users_collection = db["users"]
except errors.ConnectionError as e:
    # Handle MongoDB connection error
    app.logger.error(f"Error connecting to MongoDB: {e}")
    raise SystemExit(f"MongoDB connection failed: {e}")

# Create user
@app.route("/users", methods=["POST"])
def create_user():
    try:
        data = request.json
        if not data or "username" not in data or "email" not in data or "password" not in data:
            return jsonify({"message": "Invalid data"}), 400

        user = {
            "username": data["username"],
            "email": data["email"],
            "password": data["password"]
        }
        result = users_collection.insert_one(user)
        return jsonify({"message": "User created", "user_id": str(result.inserted_id)}), 201
    except Exception as e:
        # Catch all unexpected errors and return a detailed message
        app.logger.error(f"Error creating user: {e}")
        return jsonify({"message": "Internal server error", "error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
