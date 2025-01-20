from app.models.database import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), default='customer', nullable=False)

    # Relacionamentos
    client_tickets = db.relationship(
        'Ticket',
        foreign_keys='Ticket.client_id',
        backref='client',
        lazy=True
    )
    agent_tickets = db.relationship(
        'Ticket',
        foreign_keys='Ticket.agent_id',
        backref='agent',
        lazy=True
    )

    def __init__(self, name, email, password, role='customer'):
        self.name = name
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.role = role

    def check_password(self, password):
        """Verifica se a senha fornecida corresponde ao hash armazenado."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.name}>"
