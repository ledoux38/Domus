from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class List(db.Model):
    __tablename__ = "list"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    tag = db.Column(db.String(40), nullable=False)  # Ajout du tag sur la liste
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)
    items = db.relationship('Item', backref='list', cascade="all, delete", lazy=True)


class Suggestion(db.Model):
    __tablename__ = "suggestion"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    tag = db.Column(db.String(40), nullable=False)  # Ajout du tag pour filtrer les suggestions

    # Ajoute un index sur text et tag pour accélérer la recherche
    __table_args__ = (
        db.Index('idx_suggestion_text_tag', 'text', 'tag'),
    )


class Item(db.Model):
    __tablename__ = "item"
    id = db.Column(db.Integer, primary_key=True)
    list_id = db.Column(db.Integer, db.ForeignKey('list.id'), nullable=False)
    suggestion_id = db.Column(db.Integer, db.ForeignKey('suggestion.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1, nullable=False)
    done = db.Column(db.Boolean, default=False)
    # Optionnel : lien direct vers Suggestion pour accès facile
    suggestion = db.relationship('Suggestion')
