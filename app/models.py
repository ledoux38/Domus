from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class List(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)
    items = db.relationship('Item', backref='list', cascade="all, delete", lazy=True)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    done = db.Column(db.Boolean, default=False)
    list_id = db.Column(db.Integer, db.ForeignKey('list.id'), nullable=False)