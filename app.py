from flask import Flask, request, jsonify
import sqlite3
import json
from database import init_db, get_db_connection, close_db_connection,hash_password,check_password

app = Flask(__name__)



@app.route('/')
def home():
    return "User Management System"

@app.route('/users', methods=['GET'])
def get_all_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email FROM users")
    users = cursor.fetchall()
    close_db_connection(conn)
    return jsonify([dict(user) for user in users]), 200

@app.route('/user/<user_id>', methods=['GET'])
def get_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM users WHERE id = '{user_id}'")
    user = cursor.fetchone()
    close_db_connection(conn)
    
    if user:
        return jsonify(dict(user)), 200
    else:
        return "User not found", 404

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or not all(k in data for k in ('name', 'email', 'password')):
        return jsonify({"error": "Missing data"}), 400
    
    name = data['name']
    email = data['email']
    password = data['password']
    
    hashed_pw = hash_password(password)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, hashed_pw))
        conn.commit()
        user_id = cursor.lastrowid
    except conn.IntegrityError:
        close_db_connection(conn)
        return jsonify({"error": "Email address already exists"}), 409
    finally:
        close_db_connection(conn)
    
    return jsonify({"message": "User created", "user_id": user_id}), 201

@app.route('/user/<user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    if not data or not any(k in data for k in ('name', 'email')):
        return jsonify({"error": "Invalid data"}), 400
    
    name = data.get('name')
    email = data.get('email')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET name = ?, email = ? WHERE id = ?", (name, email, user_id))
    conn.commit()
    close_db_connection(conn)
    
    return jsonify({"message": "User updated"}), 200

@app.route('/user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    close_db_connection(conn)
    
    print(f"User {user_id} deleted")
    return jsonify({"message": "User deleted"}), 200

@app.route('/search', methods=['GET'])
def search_users():
    name = request.args.get('name')
    if not name:
        return jsonify({"error": "Please provide a name to search"}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email FROM users WHERE name LIKE ?", (f"%{name}%",))
    users = cursor.fetchall()
    close_db_connection(conn)
    return jsonify([dict(user) for user in users]), 200

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not all(k in data for k in ('email', 'password')):
        return jsonify({"error": "Missing email or password"}), 400

    email = data['email']
    password = data['password']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, password FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    close_db_connection(conn)
    
    if user and check_password(password, user['password']):
        return jsonify({"status": "success", "user_id": user['id']}), 200
    else:
        return jsonify({"status": "failed", "error": "Invalid credentials"}), 401
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5009, debug=True)