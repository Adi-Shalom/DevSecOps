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
    orders_collection = db["orders"]
except errors.ConnectionError as e:
    app.logger.error(f"Error connecting to MongoDB: {e}")
    raise SystemExit(f"MongoDB connection failed: {e}")

# Create order
@app.route("/orders", methods=["POST"])
def create_order():
    try:
        data = request.json
        if not data or "product_id" not in data or "user_id" not in data or "quantity" not in data:
            return jsonify({"message": "Invalid data"}), 400

        order = {
            "product_id": data["product_id"],
            "user_id": data["user_id"],
            "quantity": data["quantity"]
        }
        result = orders_collection.insert_one(order)
        return jsonify({"message": "Order created", "order_id": str(result.inserted_id)}), 201
    except Exception as e:
        app.logger.error(f"Error creating order: {e}")
        return jsonify({"message": "Internal server error", "error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
