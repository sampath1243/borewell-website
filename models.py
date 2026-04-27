from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    phone = db.Column(db.String(15))
    service = db.Column(db.String(50))
    depth = db.Column(db.Integer)
    location = db.Column(db.String(200))
    payment_status = db.Column(db.String(20), default="Pending")