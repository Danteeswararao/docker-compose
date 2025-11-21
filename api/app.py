from flask import Flask, jsonify, request
from flask_cors import CORS
import pymysql

app = Flask(__name__)
CORS(app)

# MySQL connection settings (from env)
DB_HOST = "db"
DB_USER = "root"
DB_PASS = "example"
DB_NAME = "appdb"

def get_db_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )

# -----------------------
# CRUD Routes
# -----------------------

# Get all users
@app.route("/api/users", methods=["GET"])
def get_users():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM users")
        result = cursor.fetchall()
    conn.close()
    return jsonify(result)

# Get a single user by ID
@app.route("/api/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))
        result = cursor.fetchone()
    conn.close()
    if result:
        return jsonify(result)
    return jsonify({"error": "User not found"}), 404

# Create a new user
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

# Update a user
@app.route("/api/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")

    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))
        if not cursor.fetchone():
            return jsonify({"error": "User not found"}), 404

        cursor.execute("UPDATE users SET name=%s, email=%s WHERE id=%s", (name, email, user_id))
        conn.commit()
    conn.close()
    return jsonify({"id": user_id, "name": name, "email": email})

# Delete a user
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

if __name__ == "__main__":
    # Must bind to 0.0.0.0 in Docker
    app.run(host="0.0.0.0", port=5000)
