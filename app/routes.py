from flask import Blueprint, render_template, request, redirect, url_for
from .models import db, List, Suggestion, Item

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    return render_template('index.html')


# 1. Voir toutes les listes
@bp.route('/lists')
def all_lists():
    lists = List.query.all()
    return render_template('lists.html', lists=lists)


# 2. Créer une nouvelle liste (avec tag)
@bp.route('/list/new', methods=['POST'])
def add_list():
    name = request.form.get('name')
    tag = request.form.get('tag')
    if name and tag:
        list_ = List(name=name, tag=tag)
        db.session.add(list_)
        db.session.commit()
    return redirect(url_for('main.all_lists'))


# 3. Renommer une liste
@bp.route('/list/rename/<int:list_id>', methods=['PUT'])
def rename_list(list_id):
    name = request.form.get('name')
    list_ = List.query.get_or_404(list_id)
    if name:
        list_.name = name
        db.session.commit()
    return redirect(url_for('main.all_lists'))


# 4. Voir une liste + ses items
@bp.route('/list/<int:list_id>')
def get_list(list_id):
    list_ = List.query.get_or_404(list_id)
    items = Item.query.filter_by(list_id=list_.id).all()
    return render_template('list_detail.html', list=list_, items=items)


# 5. Supprimer une liste
@bp.route('/lists/<int:list_id>/delete', methods=['POST'])
def delete_list(list_id):
    list_ = List.query.get_or_404(list_id)
    db.session.delete(list_)
    db.session.commit()
    return redirect(url_for('main.all_lists'))


# 6. Ajouter un item (association avec Suggestion)
@bp.route('/lists/<int:list_id>/add_item', methods=['POST'])
def add_item(list_id):
    text = request.form.get('text')
    list_ = List.query.get_or_404(list_id)
    if not text:
        return redirect(url_for('main.get_list', list_id=list_id))
    tag = list_.tag
    # 1. Cherche la suggestion existante pour ce texte/tag (insensible à la casse)
    suggestion = Suggestion.query.filter(
        db.func.lower(Suggestion.text) == text.lower(),
        Suggestion.tag == tag
    ).first()
    # 2. Si non trouvée, crée la suggestion
    if not suggestion:
        suggestion = Suggestion(text=text, tag=tag)
        db.session.add(suggestion)
        db.session.commit()
    # 3. Cherche si déjà dans la liste (association existante)
    item = Item.query.filter_by(list_id=list_id, suggestion_id=suggestion.id).first()
    if item:
        item.quantity += 1
    else:
        item = Item(list_id=list_id, suggestion_id=suggestion.id, quantity=1)
        db.session.add(item)
    db.session.commit()
    return redirect(url_for('main.get_list', list_id=list_id))


# 7. Toggle fait/pas fait sur un item
@bp.route('/lists/<int:list_id>/item/<int:item_id>/toggle', methods=['POST'])
def toggle_item(list_id, item_id):
    item = Item.query.get_or_404(item_id)
    item.done = not item.done
    db.session.commit()
    return redirect(url_for('main.get_list', list_id=list_id))


# 8. Supprimer un item (décrémente quantité ou supprime l'association si quantité==1)
@bp.route('/lists/<int:list_id>/item/<int:item_id>/delete', methods=['POST'])
def delete_item(list_id, item_id):
    item = Item.query.get_or_404(item_id)
    if item.quantity > 1:
        item.quantity -= 1
    else:
        db.session.delete(item)
    db.session.commit()
    return redirect(url_for('main.get_list', list_id=list_id))


# 9. Suggestions : retourne max 5 suggestions contenant le texte, pour le tag de la liste
@bp.route('/lists/<int:list_id>/suggestions')
def get_suggestions(list_id):
    q = request.args.get('q', '')
    list_ = List.query.get_or_404(list_id)
    tag = list_.tag
    # recherche insensible à la casse, max 5 résultats
    suggestions = Suggestion.query.filter(
        Suggestion.tag == tag,
        Suggestion.text.ilike(f'%{q}%')
    ).limit(5).all()
    # retourne en JSON, à adapter selon le front
    return {'suggestions': [s.text for s in suggestions]}


# 10. (Optionnel) Clear suggestions for a tag
@bp.route('/suggestions/<tag>/clear', methods=['POST'])
def clear_suggestions(tag):
    Suggestion.query.filter_by(tag=tag).delete()
    db.session.commit()
    return redirect(url_for('main.all_lists'))
