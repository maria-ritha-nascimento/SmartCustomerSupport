from flask import Blueprint, jsonify, request, session
from app.models.database import db
from app.models.user import User
from app.utils.auth import hash_password, verify_password, login_required

api_bp = Blueprint('api', __name__)

@api_bp.route('/ping', methods=['GET'])
def ping():
    return jsonify({'message': 'pong'}), 200

@api_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    role = data.get('role', 'customer')  # Por padrão, o usuário será um cliente
    if role not in ['customer', 'agent']:
    return jsonify({'error': 'Invalid role specified.'}), 400
    hashed_password = hash_password(data['password'])
    user = User(name=data['name'], email=data['email'], password=hashed_password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

@api_bp.route('/users', methods=['GET'])
@login_required
def get_users():
    users = User.query.all()
    return jsonify([{'id': u.id, 'name': u.name, 'email': u.email} for u in users]), 200

@api_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and verify_password(data['password'], user.password):
        session['user_id'] = user.id
        return jsonify({
            'message': 'Login successful',
            'user': {
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'role': user.role
            }
        }), 200
    return jsonify({'error': 'Invalid credentials'}), 401
