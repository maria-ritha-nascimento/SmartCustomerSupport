from app.models.database import db

class Ticket(db.Model):
    __tablename__ = 'tickets'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='open')
    client_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # Defina antes de usar
    agent_id = db.Column(db.Integer, db.ForeignKey('users.id'))   # Defina antes de usar
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    # Relacionamentos definidos após as colunas
    client = db.relationship('app.models.user.User', foreign_keys=[client_id], backref='submitted_tickets')
    agent = db.relationship('app.models.user.User', foreign_keys=[agent_id], backref='assigned_tickets')
