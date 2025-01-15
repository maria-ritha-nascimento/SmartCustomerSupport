from flask import Blueprint, jsonify, request, session
from app.models.database import db
from app.models.user import User
from functools import wraps

api_bp = Blueprint('api', __name__)

# Decorador para proteger rotas
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({"error": "Unauthorized access. Please log in."}), 401
        return f(*args, **kwargs)
    return decorated_function

@api_bp.route('/ping', methods=['GET'])
def ping():
    return jsonify({"message": "Pong!", "status": "success"})

# Rotas para CRUD de usuários
@api_bp.route('/users', methods=['POST'])
@login_required
def create_user():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not name or not email or not password:
        return jsonify({"error": "Missing required fields"}), 400

    # Verificar se o e-mail já existe
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already in use"}), 400

    user = User(name=name, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User created successfully", "user": {"id": user.id, "name": user.name, "email": user.email}}), 201

@api_bp.route('/users', methods=['GET'])
@login_required
def get_users():
    users = User.query.all()
    user_list = [{"id": user.id, "name": user.name, "email": user.email} for user in users]
    return jsonify(user_list), 200

@api_bp.route('/users/<int:user_id>', methods=['GET'])
@login_required
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"id": user.id, "name": user.name, "email": user.email}), 200

@api_bp.route('/users/<int:user_id>', methods=['PUT'])
@login_required
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    user.name = data.get('name', user.name)
    user.email = data.get('email', user.email)
    if 'password' in data:
        user.set_password(data['password'])
    db.session.commit()

    return jsonify({"message": "User updated successfully", "user": {"id": user.id, "name": user.name, "email": user.email}}), 200

@api_bp.route('/users/<int:user_id>', methods=['DELETE'])
@login_required
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "User deleted successfully"}), 200

# Rota de login
@api_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Missing email or password"}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid email or password"}), 401

    session['user_id'] = user.id
    return jsonify({"message": "Login successful", "user": {"id": user.id, "name": user.name, "email": user.email}}), 200

# Rota de logout
@api_bp.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify({"message": "Logout successful"}), 200