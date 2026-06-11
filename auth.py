from flask import jsonify, request
from app import app
import models
from werkzeug.security import generate_password_hash, check_password_hash

def hash_password(plain_password: str, method: str = 'scrypt', salt_length: int = 16) -> str:
    if not plain_password:
        raise ValueError("Password should be non-empty")
    return generate_password_hash(plain_password, method=method, salt_length=salt_length)

def verify_password(stored_password: str, provided_password: str) -> bool:
    if not stored_password or not provided_password:
        return False
    return check_password_hash(stored_password, provided_password)


@app.route('/auth/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return jsonify({"message": "Send POST with username, email, password"}), 200

    data = request.get_json() or {}
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({"error": "username, email, and password are required"}), 400

    existing = models.User.query.filter_by(email=email).first()
    if existing:
        return jsonify({"error": "Email already registered"}), 400

    user = models.User(
        username=username,
        email=email,
        password=hash_password(password),
    )
    models.db.session.add(user)
    models.db.session.commit()

    return jsonify({"message": "User registered successfully", "user_id": user.id}), 201


@app.route('/auth/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return jsonify({"message": "Send POST with email and password"}), 200

    data = request.get_json() or {}
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "email and password are required"}), 400

    user = models.User.query.filter_by(email=email).first()
    if not user or not verify_password(user.password, password):
        return jsonify({"error": "Invalid email or password"}), 401

    return jsonify({"message": "Login successful", "user_id": user.id, "username": user.username}), 200