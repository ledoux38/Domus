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
    items = Item.query.filter_by(liste_id=liste.id).all()
    return render_template('liste_detail.html', liste=liste, items=items)


@bp.route('/listes/<int:liste_id>/supprimer', methods=['POST'])
def supprimer_liste(liste_id):
    liste = Liste.query.get_or_404(liste_id)
    db.session.delete(liste)
    db.session.commit()
    return redirect(url_for('main.toutes_les_listes'))


@bp.route('/listes/<int:liste_id>/ajouter_item', methods=['POST'])
def ajouter_item(liste_id):
    texte = request.form.get('texte')
    if texte:
        item = Item(texte=texte, liste_id=liste_id)
        db.session.add(item)
        db.session.commit()
    return redirect(url_for('main.voir_liste', liste_id=liste_id))


@bp.route('/listes/<int:liste_id>/item/<int:item_id>/toggle', methods=['POST'])
def toggle_item(liste_id, item_id):
    item = Item.query.get_or_404(item_id)
    item.fait = not item.fait
    db.session.commit()
    return redirect(url_for('main.voir_liste', liste_id=liste_id))


@bp.route('/listes/<int:liste_id>/item/<int:item_id>/supprimer', methods=['POST'])
def supprimer_item(liste_id, item_id):
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('main.voir_liste', liste_id=liste_id))