from flask import Flask, jsonify, request
from flask_cors import CORS
import pymysql
import os
import time

app = Flask(__name__)
CORS(app)

# ----------------------------
# Database configuration
# ----------------------------
DB_HOST = os.environ.get("DB_HOST", "db")
DB_USER = os.environ.get("DB_USER", "root")
DB_PASS = os.environ.get("DB_PASS", "example")
DB_NAME = os.environ.get("DB_NAME", "appdb")

# Wait for DB to be ready
def wait_for_db(retries=10, delay=2):
    for _ in range(retries):
        try:
            conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME)
            conn.close()
            return
        except pymysql.err.OperationalError:
            print("Waiting for database...")
            time.sleep(delay)
    raise Exception("Database not available after multiple retries")

wait_for_db()

def get_db_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )

# ----------------------------
# CRUD Routes
# ----------------------------

# Health check
@app.route("/api/", methods=["GET"])
def home():
    return jsonify({"message": "API is running"})


# GET all users
@app.route("/api/users", methods=["GET"])
def get_users():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
    conn.close()
    return jsonify(users)


# GET single user by ID
@app.route("/api/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))
        user = cursor.fetchone()
    conn.close()
    if user:
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404


# POST create new user
@app.route("/api/users", methods=["POST"])
def create_user():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    if not name or not email:
        return jsonify({"error": "Name and email are required"}), 400

    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
        conn.commit()
        user_id = cursor.lastrowid
    conn.close()
    return jsonify({"id": user_id, "name": name, "email": email}), 201


# PUT update existing user
@app.route("/api/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    if not name or not email:
        return jsonify({"error": "Name and email are required"}), 400

    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))
        if not cursor.fetchone():
            return jsonify({"error": "User not found"}), 404

        cursor.execute("UPDATE users SET name=%s, email=%s WHERE id=%s", (name, email, user_id))
        conn.commit()
    conn.close()
    return jsonify({"id": user_id, "name": name, "email": email})


# DELETE user
@app.route("/api/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))
        if not cursor.fetchone():
            return jsonify({"error": "User not found"}), 404

        cursor.execute("DELETE FROM users WHERE id=%s", (user_id,))
        conn.commit()
    conn.close()
    return jsonify({"message": f"User {user_id} deleted"})


# ----------------------------
# Start Flask app
# ----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
