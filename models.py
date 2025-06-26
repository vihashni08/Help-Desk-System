from extensions import db  # ✅ import db from extensions.py

class User(db.Model):
    __tablename__ = 'users'
    email = db.Column(db.String(120), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Ticket(db.Model):
    __tablename__ = 'tickets'
    id = db.Column(db.String(6), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    room = db.Column(db.String(20), nullable=False)
    mobile = db.Column(db.String(15), nullable=False)
    time = db.Column(db.String(20), nullable=False)
    priority = db.Column(db.Boolean, default=False)
    email = db.Column(db.String(120), db.ForeignKey('users.email'))
