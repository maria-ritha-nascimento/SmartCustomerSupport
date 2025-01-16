from flask import Blueprint, jsonify, request, session
from app.models.database import db
from app.models.user import User
from app.utils.auth import hash_password, verify_password, login_required, role_required

api_bp = Blueprint('api', __name__)

@api_bp.route('/ping', methods=['GET'])
def ping():
    return jsonify({'message': 'Pong!'}), 200


@api_bp.route('/users', methods=['POST'])
def create_user():
    """
    Endpoint para criar um novo usuário no sistema.
    """
    data = request.get_json()
    role = data.get('role', 'customer')  # Por padrão, o usuário será um cliente
    if role not in ['customer', 'agent']:
        return jsonify({'error': 'Invalid role specified.'}), 400

    hashed_password = hash_password(data['password'])
    user = User(name=data['name'], email=data['email'], password=hashed_password, role=role)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created successfully', 'role': role}), 201


@api_bp.route('/users', methods=['GET'])
@login_required
def get_users():
    """
    Endpoint para listar todos os usuários cadastrados.
    Requer autenticação.
    """
    users = User.query.all()
    users_data = [
        {'id': user.id, 'name': user.name, 'email': user.email, 'role': user.role}
        for user in users
    ]
    return jsonify(users_data), 200


@api_bp.route('/login', methods=['POST'])
def login():
    """
    Endpoint para autenticar um usuário com e-mail e senha.
    """
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


@api_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    """
    Endpoint para fazer logout do usuário autenticado.
    """
    session.pop('user_id', None)
    return jsonify({'message': 'Logout successful'}), 200


@api_bp.route('/agents-only', methods=['GET'])
@role_required('agent')
def agents_only():
    """
    Endpoint disponível apenas para usuários com o papel de 'agent'.
    """
    return jsonify({'message': 'Hello, agent!'}), 200
