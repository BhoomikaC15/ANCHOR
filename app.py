from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
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
            return jsonify({"error": "Email already registered"}), 400
        user.email=email
    models.db.session.commit()

@app.route('/users/<int:user_id>', methods=["DELETE"])
def delete_user(user_id):
    user=models.User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    models.db.session.delete(user)
    models.db.session.commit()
    return jsonify({"message": "User deleted successfully"}), 200


#API's for Category model
@app.route('/categories', methods=['POST'])
def create_category():
    data=request.get_json()
    name=data.get("name")
    user_id=data.get("user_id")
    if not name or not user_id:
        return jsonify({"error": "Fields cannot be left empty"}), 400
    user=models.User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 400
    category=models.Category(
        name=name,
        user_id=user_id
    )
    models.db.session.add(category)
    models.db.session.commit()
    return jsonify({
        "id": category.id,
        "name": category.name,
        "user_id": category.user_id
    }), 201

@app.route('/users/<int:user_id>/categories', methods=['GET'])
def get_categories_by_user(user_id):
    user=models.User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    categories=models.Category.query.filter_by(user_id=user_id).all()
    result=[]
    for category in categories:
        result.append({
            "id": category.id,
            "name": category.name,
            "user_id": category.user_id
        })
    return jsonify(result), 200

@app.route('/categories/<int:category_id>', methods=['GET'])
def get_category_by_id(category_id):
    category=models.Category.query.get(category_id)
    if not category:
        return jsonify({"error": "Category not found"}), 404
    return jsonify({
        "id": category.id,
        "name": category.name,
        "user_id": category.user_id
    }), 200

@app.route('/categories/<int:category_id>', methods=['PUT'])
def update_category(category_id):
    category=models.Category.query.get(category_id)
    if not category:
        return jsonify({"error": "Category not found"}), 404
    data=request.get_json()
    name=data.get("name")
    if name:
        category.name=name
    models.db.session.commit()
    return jsonify({
        "id": category.id,
        "name": category.name,
        "user_id": category.user_id
    }), 200

@app.route('/categories/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    category=models.Category.query.get(category_id)
    if not category:
        return jsonify({"error": "Category not found"}), 400
    models.db.session.delete(category)
    models.db.session.commit()
    return jsonify({"message": "category successfully deleted"}), 200


#API's for Session model
@app.route('/sessions', methods=['POST'])
def create_session():
    data=request.get_json()
    user_id=data.get("user_id")
    category_id=data.get("category_id")
    duration_min=data.get("duration_min")
    date=data.get("date")
    if not user_id or not category_id or not duration_min or not date:
        return jsonify({"error": "Fields cannot be left empty"}), 400
    if not user_id:
        return jsonify({"error": "User not found"}), 404
    if not category_id:
        return jsonify({"error": "Category not found"}), 404
    try:
        session_date=datetime.strptime(date, "%d-%m-%Y").date()
    except ValueError:
        return jsonify({"error": "Date must be in format DD-MM-YYYY"}),400
    ses=models.Session(
        user_id=user_id,
        category_id=category_id,
        duration_min=duration_min,
        date=session_date
    )
    models.db.session.add(ses)
    models.db.session.commit()
    return jsonify({
        "id": ses.id,
        "user_id": ses.user_id,
        "category_id": ses.category_id,
        "duration_min": ses.duration_min,
        "date": ses.date.isoformat()
    }), 201

@app.route('/sessions', methods=['GET'])
def get_sessions():
    user_id=request.args.get("user_id", type=int)
    category_id=request.args.get("category_id", type=int)
    query=models.Session.query
    if user_id is not None:
        query=query.filter_by(user_id=user_id)
    if category_id is not None:
        query=query.filter_by(category_id=category_id)
    sessions=query.all()
    result=[]
    for ses in sessions:
        result.append({
            "id": ses.id,
            "user_id": ses.user_id,
            "category_id": ses.category_id,
            "duration_min": ses.duration_min,
            "date": ses.date.isoformat()
        })
    return jsonify(result), 200

@app.route('/users/<int:user_id>/sessions', methods=['GET'])
def get_sessions_by_user(user_id):
    user=models.User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    sessions=models.Session.query.filter_by(user_id=user_id).all()
    result=[]
    for ses in sessions:
        result.append({
            "id": ses.id,
            "user_id": ses.user_id,
            "category_id": ses.category_id,
            "duration_min": ses.duration_min,
            "date": ses.date.isoformat()
        })
    return jsonify(result), 200

@app.route('/sessions/<int:session_id>', methods=['GET'])
def get_session_by_id(session_id):
    ses=models.Session.query.get(session_id)
    if not ses:
        return jsonify({"error": "Session not found"}), 404
    return jsonify({
        "id": ses.id,
        "user_id": ses.user_id,
        "category_id": ses.category_id,
        "duration_min": ses.duration_min,
        "date": ses.date.isoformat()
    }), 200

@app.route('/sessions/<int:session_id>', methods=['PUT'])
def update_session(session_id):
    ses=models.Session.query.get(session_id)
    if not ses:
        return jsonify({"error": "Session not found"}), 404
    data=request.get_json()
    category_id=data.get("category_id")
    duration_min=data.get("duration_min")
    date=data.get("date")   
    if category_id:
        new_cat=models.Category.query.get(category_id)
        if not new_cat:
            return jsonify({"error": "Category not found"}), 404
        ses.category_id=category_id
    if duration_min:
        ses.duration_min=duration_min
    if date:
        try:
            ses.date=datetime.strptime(date, "%d-%m-%Y").date()
        except ValueError:
            return jsonify({"error": "Date must be in format DD-MM-YYYY"}),400

    models.db.session.commit()
    return jsonify({
        "id": ses.id,
        "user_id": ses.user_id,
        "category_id": ses.category_id,
        "duration_min": ses.duration_min,
        "date": ses.date.isoformat()
    }), 200

@app.route('/sessions/<int:session_id>', methods=['DELETE'])
def delete_session(session_id):
    ses=models.Session.query.get(session_id)
    if not ses:
        return jsonify({"error": "session not found"}), 404
    models.db.session.delete(ses)
    models.db.session.commit()
    return jsonify({"message": "Session successfully deleted"}), 200

if __name__== "__main__":
    with app.app_context():
        models.db.create_all()
    app.run(debug=True)