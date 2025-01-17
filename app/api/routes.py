from flask import Blueprint, jsonify, request, session
from app.models.database import db
from app.models.user import User
from app.models.ticket import Ticket
from app.utils.auth import hash_password, verify_password, login_required, role_required

api_bp = Blueprint('api', __name__)

@api_bp.route('/ping', methods=['GET'])
def ping():
    """
    Verifica a conectividade com o servidor.
    """
    return jsonify({'message': 'Pong!'}), 200

@api_bp.route('/users', methods=['POST'])
def create_user():
    """
    Endpoint para criar um novo usuário no sistema.
    """
    data = request.get_json()

    # Validações
    if not data or not data.get('name') or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Name, email, and password are required.'}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists.'}), 400

    role = data.get('role', 'customer').lower()
    if role not in ['customer', 'agent']:
        return jsonify({'error': 'Invalid role specified. Valid roles: customer, agent.'}), 400

    # Criação do usuário
    hashed_password = hash_password(data['password'])
    user = User(name=data['name'], email=data['email'], password=hashed_password, role=role)
    db.session.add(user)
    db.session.commit()

    return jsonify({
        'message': 'User created successfully',
        'user': {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'role': user.role
        }
    }), 201

@api_bp.route('/users', methods=['GET'])
@login_required
def get_users():
    """
    Endpoint para listar todos os usuários cadastrados.
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

    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password are required.'}), 400

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

@api_bp.route('/tickets', methods=['POST'])
@login_required
@role_required('customer')
def create_ticket():
    """
    Endpoint para criar um ticket.
    """
    data = request.get_json()
    if not data or not data.get('title') or not data.get('description'):
        return jsonify({'error': 'Title and description are required.'}), 400

    client_id = session['user_id']
    ticket = Ticket(title=data['title'], description=data['description'], client_id=client_id)
    db.session.add(ticket)
    db.session.commit()

    return jsonify({'message': 'Ticket created successfully', 'ticket_id': ticket.id}), 201

@api_bp.route('/tickets', methods=['GET'])
@login_required
def get_tickets():
    """
    Endpoint para listar todos os tickets.
    Clientes veem apenas seus tickets; atendentes veem todos.
    """
    user_id = session['user_id']
    user = User.query.get(user_id)

    if user.role == 'customer':
        tickets = Ticket.query.filter_by(client_id=user_id).all()
    elif user.role == 'agent':
        tickets = Ticket.query.all()

    tickets_data = [
        {
            'id': ticket.id,
            'title': ticket.title,
            'description': ticket.description,
            'status': ticket.status,
            'client_id': ticket.client_id,
            'agent_id': ticket.agent_id,
            'created_at': ticket.created_at,
            'updated_at': ticket.updated_at
        }
        for ticket in tickets
    ]

    return jsonify(tickets_data), 200

@api_bp.route('/tickets/<int:ticket_id>', methods=['PUT'])
@login_required
@role_required('agent')
def update_ticket(ticket_id):
    """
    Endpoint para atualizar um ticket.
    Apenas atendentes podem atualizar tickets.
    """
    data = request.get_json()
    ticket = Ticket.query.get(ticket_id)

    if not ticket:
        return jsonify({'error': 'Ticket not found.'}), 404

    if data.get('status') not in ['open', 'in_progress', 'closed']:
        return jsonify({'error': 'Invalid status. Valid values: open, in_progress, closed.'}), 400

    ticket.status = data.get('status', ticket.status)
    ticket.agent_id = session['user_id']
    db.session.commit()

    return jsonify({'message': 'Ticket updated successfully'}), 200

@api_bp.route('/tickets/<int:ticket_id>', methods=['DELETE'])
@login_required
@role_required('agent')
def delete_ticket(ticket_id):
    """
    Endpoint para excluir um ticket.
    Apenas atendentes podem excluir tickets.
    """
    ticket = Ticket.query.get(ticket_id)

    if not ticket:
        return jsonify({'error': 'Ticket not found.'}), 404

    db.session.delete(ticket)
    db.session.commit()

    return jsonify({'message': 'Ticket deleted successfully'}), 200

@api_bp.route('/agents-only', methods=['GET'])
@role_required('agent')
def agents_only():
    """
    Endpoint disponível apenas para usuários com o papel de 'agent'.
    """
    return jsonify({'message': 'Hello, agent!'}), 200
