from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import date
import models

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///productivity.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

models.db.init_app(app)

#API's for User model
@app.route('/users', methods=['POST'])
def create_user():
    data=request.get_json()
    username= data.get("username")
    email=data.get("email")
    password=data.get("password")
    if not username or not email or not password:
        return jsonify({"error": "Fields can't be empty"}), 400
    existing= models.User.query.filter_by(email=email).first()
    if existing:
        return jsonify({"error": "Email already registered"}), 400
    user=models.User(
        username=username,
        email=email,
        password=password
    )
    models.db.session.add(user)
    models.db.session.commit()
    return jsonify({"message": "User created successfully"}), 201

@app.route('/users', methods=['GET'])
def get_all_users():
    users=models.User.query.all()
    result=[]
    for user in users:
        result.append({
            "id": user.id,
            "username": user.username, 
            "email": user.email,
            "created_at": user.created_at
        })
    return jsonify(result), 200

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    user=models.User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify({
        "id":user.id,
        "username":user.username,
        "email":user.email,
        "created_at":user.created_at
    }), 200

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user=models.User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 400
    data=request.get_json()
    username=data.get("username")
    email=data.get("email")
    if username:
        user.username=username
    if email:
        existing=models.User.query.filter_by(email=email).first()
        if existing and existing.id != user_id:
            return jsonify({"error": "Email already registred"}), 400
        user.email=email
    models.db.commit()

@app.route('/users/<int:user_id>', methods=["DELETE"])
def delete_user(user_id):
    user=models.User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    models.db.session.delete(user)
    models.db.session.commit(user)
    return jsonify({"message": "User deleted successfully"}), 200

if __name__== "__main__":
    with app.app_context():
        models.db.create_all()
    app.run(debug=True)