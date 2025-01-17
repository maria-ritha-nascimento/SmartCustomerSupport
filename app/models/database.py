from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

def init_db(app):
    """
    Inicializa o banco de dados com o app Flask.
    """
    db.init_app(app)
    with app.app_context():
        db.create_all()  # Certifica-se de que as tabelas sejam criadas.

# Modelos
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # Roles: client, agent, admin
    tickets_created = db.relationship('Ticket', foreign_keys='Ticket.client_id', backref='client', lazy=True)
    tickets_assigned = db.relationship('Ticket', foreign_keys='Ticket.agent_id', backref='agent', lazy=True)

class Ticket(db.Model):
    __tablename__ = 'ticket'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default="open")  # Status: open, in_progress, closed
    client_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Cliente que criou o ticket
    agent_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  # Atendente responsável
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
