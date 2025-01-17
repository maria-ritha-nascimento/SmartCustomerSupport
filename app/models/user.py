from app.models.database import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), default='customer', nullable=False)

    # Relacionamentos
    client_tickets = db.relationship('Ticket', foreign_keys='Ticket.client_id', backref='client', lazy=True)
    agent_tickets = db.relationship('Ticket', foreign_keys='Ticket.agent_id', backref='agent', lazy=True)

    def __repr__(self):
        return f"<User {self.name}>"
