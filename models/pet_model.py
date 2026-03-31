from config.db import db

class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    breed = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    owner_id = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(300))