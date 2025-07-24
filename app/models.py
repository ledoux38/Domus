from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

list_tag = db.Table(
    "list_tag",
    db.Column("list_id", db.Integer, db.ForeignKey("list.id"), primary_key=True),
    db.Column("tag_id", db.Integer, db.ForeignKey("tag.id"), primary_key=True),
)

suggestion_tag = db.Table(
    "suggestion_tag",
    db.Column("suggestion_id", db.Integer, db.ForeignKey("suggestion.id"), primary_key=True),
    db.Column("tag_id", db.Integer, db.ForeignKey("tag.id"), primary_key=True),
)

class List(db.Model):
    __tablename__ = "list"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)
    items = db.relationship('Item', backref='list', cascade="all, delete", lazy=True)
    tags = db.relationship("Tag", secondary=list_tag, backref="lists")


class Suggestion(db.Model):
    __tablename__ = "suggestion"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    __table_args__ = (
        db.Index('idx_suggestion_text', 'text'),
    )
    tags = db.relationship("Tag", secondary=suggestion_tag, backref="suggestions")


class Item(db.Model):
    __tablename__ = "item"
    id = db.Column(db.Integer, primary_key=True)
    list_id = db.Column(db.Integer, db.ForeignKey('list.id'), nullable=False)
    suggestion_id = db.Column(db.Integer, db.ForeignKey('suggestion.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1, nullable=False)
    done = db.Column(db.Boolean, default=False)
    suggestion = db.relationship('Suggestion')


class Tag(db.Model):
    __tablename__ = "tag"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True, nullable=False)