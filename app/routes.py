from flask import Blueprint, render_template, request, redirect, url_for
from .models import db, Liste, Item

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/listes')
def toutes_les_listes():
    listes = Liste.query.all()
    return render_template('listes.html', listes=listes)

@bp.route('/listes/nouvelle', methods=['POST'])
def ajouter_liste():
    nom = request.form.get('nom')
    if nom:
        liste = Liste(nom=nom)
        db.session.add(liste)
        db.session.commit()
    return redirect(url_for('main.toutes_les_listes'))

@bp.route('/listes/<int:liste_id>')
def voir_liste(liste_id):
    liste = Liste.query.get_or_404(liste_id)
    return render_template('liste_detail.html', liste=liste)

@bp.route('/listes/<int:liste_id>/supprimer', methods=['POST'])
def supprimer_liste(liste_id):
    liste = Liste.query.get_or_404(liste_id)
    db.session.delete(liste)
    db.session.commit()
    return redirect(url_for('main.toutes_les_listes'))