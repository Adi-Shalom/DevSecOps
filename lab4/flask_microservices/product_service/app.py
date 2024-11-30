import os
from flask import Flask, request, jsonify
from pymongo import MongoClient, errors

app = Flask(__name__)

# MongoDB URI (using environment variable for flexibility)
mongo_uri = os.getenv('MONGO_URI', 'mongodb://root:example@mongodb:27017/flask_microservices')

try:
    # Connect to MongoDB
    client = MongoClient(mongo_uri)
    db = client["flask_microservices"]
    products_collection = db["products"]
except errors.ConnectionError as e:
    app.logger.error(f"Error connecting to MongoDB: {e}")
    raise SystemExit(f"MongoDB connection failed: {e}")

# Add product
@app.route("/products", methods=["POST"])
def add_product():
    try:
        data = request.json
        if not data or "name" not in data or "price" not in data or "description" not in data:
            return jsonify({"message": "Invalid data"}), 400

        product = {
            "name": data["name"],
            "price": data["price"],
            "description": data["description"]
        }
        result = products_collection.insert_one(product)
        return jsonify({"message": "Product added", "product_id": str(result.inserted_id)}), 201
    except Exception as e:
        app.logger.error(f"Error adding product: {e}")
        return jsonify({"message": "Internal server error", "error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
