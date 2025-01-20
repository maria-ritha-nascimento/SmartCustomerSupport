from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from flask import session, jsonify
from app.models.user import User  # Importar o modelo User para consultas no banco de dados

def hash_password(password):
    """Gera um hash seguro para a senha."""
    return generate_password_hash(password)

def verify_password(password, hashed_password):
    """Verifica se a senha fornecida corresponde ao hash armazenado."""
    return check_password_hash(hashed_password, password)

def login_required(f):
    """Decorator para garantir que o usuário esteja logado."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'Unauthorized access. Please log in.'}), 401
        
        # Verifica se o usuário existe no banco de dados
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'Unauthorized access. User not found.'}), 401
        
        return f(*args, **kwargs)
    return decorated_function

def role_required(required_role):
    """Decorator para restringir o acesso com base no papel do usuário."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_id = session.get('user_id')
            if not user_id:
                return jsonify({'error': 'Unauthorized access. Please log in.'}), 401
            
            # Busca o usuário no banco de dados
            user = User.query.get(user_id)
            if not user:
                return jsonify({'error': 'Unauthorized access. User not found.'}), 401
            
            # Verifica se o papel do usuário corresponde ao papel requerido
            if user.role != required_role:
                return jsonify({'error': f'Access restricted to {required_role} role only.'}), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def any_role_required(*roles):
    """Decorator para permitir acesso a múltiplos papéis."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_id = session.get('user_id')
            if not user_id:
                return jsonify({'error': 'Unauthorized access. Please log in.'}), 401
            
            # Busca o usuário no banco de dados
            user = User.query.get(user_id)
            if not user:
                return jsonify({'error': 'Unauthorized access. User not found.'}), 401
            
            # Verifica se o papel do usuário está na lista permitida
            if user.role not in roles:
                return jsonify({'error': f'Access restricted to roles: {", ".join(roles)}.'}), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator
