from flask import Blueprint, request, jsonify
from config.db import db
from models.user_model import User
import bcrypt
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__)

# ---------------- REGISTER ----------------
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Missing fields"}), 400

    # 🔐 Hash password
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    user = User(username=username, password=hashed_pw.decode('utf-8'))

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"})


# ---------------- LOGIN ----------------
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')

    # 🔍 Find user in DB
    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    # 🔐 Check password
    if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        return jsonify({"error": "Invalid credentials"}), 401

    # 🎟️ Generate JWT token
    access_token = create_access_token(identity=str(user.id))

    return jsonify({"token": access_token})

from flask_jwt_extended import jwt_required, get_jwt_identity

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    user_id = get_jwt_identity()

    return jsonify({
        "message": "Access granted",
        "user_id": user_id
    })