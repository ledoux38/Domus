from flask import Blueprint, render_template, request, redirect, url_for, jsonify

from .models import db, List, Suggestion, Item, Tag

bp = Blueprint('main', __name__)

def get_or_create_tags(tag_string):
    tags = [t.strip() for t in tag_string.split(',') if t.strip()]
    if not tags:
        tags = ['indefinie']
    tag_objs = []
    for tag_name in tags:
        tag = Tag.query.filter_by(name=tag_name).first()
        if not tag:
            tag = Tag(name=tag_name)
            db.session.add(tag)
    db.session.commit()
    for tag_name in tags:
        tag = Tag.query.filter_by(name=tag_name).first()
        tag_objs.append(tag)
    return tag_objs


@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/lists')
def all_lists():
    lists = List.query.all()
    return render_template('lists.html', lists=lists)

@bp.route('/list/new', methods=['POST'])
def add_list():
    name = request.form.get('name')
    tag_string = request.form.get('tags', '')
    if name:
        tag_objs = get_or_create_tags(tag_string)
        list_ = List(name=name)
        list_.tags = tag_objs
        db.session.add(list_)
        db.session.commit()
    return redirect(url_for('main.all_lists'))



@bp.route('/list/rename/<int:list_id>', methods=['POST'])
def rename_list(list_id):
    name = request.form.get('name')
    list_ = List.query.get_or_404(list_id)
    if name:
        list_.name = name
        db.session.commit()
    return redirect(url_for('main.all_lists'))



@bp.route('/list/<int:list_id>')
def get_list(list_id):
    list_ = List.query.get_or_404(list_id)
    items = Item.query.filter_by(list_id=list_.id).all()
    return render_template('list_detail.html', list=list_, items=items)



@bp.route('/lists/<int:list_id>/delete', methods=['POST'])
def delete_list(list_id):
    list_ = List.query.get_or_404(list_id)
    db.session.delete(list_)
    db.session.commit()
    return redirect(url_for('main.all_lists'))


@bp.route('/lists/<int:list_id>/add_item', methods=['POST'])
def add_item(list_id):
    text = request.form.get('text')
    list_ = List.query.get_or_404(list_id)
    if not text:
        return redirect(url_for('main.get_list', list_id=list_id))
    # Récupère tous les tags de la liste
    list_tags = list_.tags or [Tag.query.filter_by(name='indefinie').first()]
    # Recherche une suggestion existante avec ce texte ET au moins un des tags de la liste
    suggestion = Suggestion.query.filter(
        Suggestion.text.ilike(text)
    ).filter(
        Suggestion.tags.any(Tag.id.in_([t.id for t in list_tags]))
    ).first()
    if not suggestion:
        suggestion = Suggestion(text=text)
        suggestion.tags = list_tags
        db.session.add(suggestion)
        db.session.commit()
    # Cherche si déjà dans la liste (association existante)
    item = Item.query.filter_by(list_id=list_id, suggestion_id=suggestion.id).first()
    if item:
        item.quantity += 1
    else:
        item = Item(list_id=list_id, suggestion_id=suggestion.id, quantity=1)
        db.session.add(item)
    db.session.commit()
    return redirect(url_for('main.get_list', list_id=list_id))


@bp.route('/lists/<int:list_id>/item/<int:item_id>/toggle', methods=['POST'])
def toggle_item(list_id, item_id):
    item = Item.query.get_or_404(item_id)
    item.done = not item.done
    db.session.commit()
    return redirect(url_for('main.get_list', list_id=list_id))

@bp.route('/lists/<int:list_id>/item/<int:item_id>/delete', methods=['POST'])
def delete_item(list_id, item_id):
    item = Item.query.get_or_404(item_id)
    if item.quantity > 1:
        item.quantity -= 1
    else:
        db.session.delete(item)
    db.session.commit()
    return redirect(url_for('main.get_list', list_id=list_id))


@bp.route('/lists/<int:list_id>/suggestions')
def get_suggestions(list_id):
    q = request.args.get('q', '')
    list_ = List.query.get_or_404(list_id)
    tag_ids = [t.id for t in list_.tags]
    # Suggestions liées à au moins un tag de la liste et dont le texte contient q
    suggestions = Suggestion.query.filter(
        Suggestion.tags.any(Tag.id.in_(tag_ids)),
        Suggestion.text.ilike(f'%{q}%')
    ).limit(5).all()
    return jsonify({'suggestions': [s.text for s in suggestions]})


@bp.route('/suggestions/<tag>/clear', methods=['POST'])
def clear_suggestions(tag):
    tag_obj = Tag.query.filter_by(name=tag).first()
    if tag_obj:
        for suggestion in tag_obj.suggestions:
            suggestion.tags.remove(tag_obj)
        db.session.commit()
    return redirect(url_for('main.all_lists'))

@bp.route('/tags/suggestions')
def tag_suggestions():
    q = request.args.get('q', '')
    tags = Tag.query.filter(Tag.name.ilike(f'%{q}%')).limit(5).all()
    return jsonify({'suggestions': [t.name for t in tags]})