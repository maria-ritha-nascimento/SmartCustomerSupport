from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from flask import session, jsonify

def hash_password(password):
    return generate_password_hash(password)

def verify_password(password, hashed_password):
    return check_password_hash(hashed_password, password)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Unauthorized access. Please log in.'}), 401
        return f(*args, **kwargs)
    return decorated_function

def role_required(required_role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                return jsonify({'error': 'Unauthorized access. Please log in.'}), 401
            user = User.query.get(session['user_id'])
            if user.role != required_role:
                return jsonify({'error': f'Access restricted to {required_role} only.'}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator
