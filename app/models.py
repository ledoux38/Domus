from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Liste(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(80), nullable=False)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    items = db.relationship('Item', backref='liste', cascade="all, delete", lazy=True)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    texte = db.Column(db.String(200), nullable=False)
    fait = db.Column(db.Boolean, default=False)
    liste_id = db.Column(db.Integer, db.ForeignKey('liste.id'), nullable=False)