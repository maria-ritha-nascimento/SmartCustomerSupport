from app.models.database import db
from datetime import datetime

class Ticket(db.Model):
    __tablename__ = 'tickets'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), default='open', nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    agent_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    client = db.relationship('User', foreign_keys=[client_id], backref='client_tickets')
    agent = db.relationship('User', foreign_keys=[agent_id], backref='agent_tickets')

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'client_id': self.client_id,
            'agent_id': self.agent_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
