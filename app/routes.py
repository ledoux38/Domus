from flask import Blueprint, request, jsonify
from .models import db, List, Suggestion, Item, Tag
from .utils import serialize_list, serialize_item, get_or_create_tags, serialize_suggestion

bp = Blueprint('main', __name__)

# ------------------ ROUTES API JSON ------------------

@bp.route('/api/lists', methods=['GET'])
def api_get_lists():
    lists = List.query.all()
    return jsonify([serialize_list(lst) for lst in lists])

@bp.route('/api/lists/<int:list_id>', methods=['GET'])
def api_get_list(list_id):
    lst = List.query.get_or_404(list_id)
    return jsonify(serialize_list(lst))

@bp.route('/api/lists/<int:list_id>/items', methods=['GET'])
def api_get_items(list_id):
    lst = List.query.get_or_404(list_id)
    items = Item.query.filter_by(list_id=lst.id).all()
    return jsonify([serialize_item(i) for i in items])

@bp.route('/api/lists', methods=['POST'])
def api_add_list():
    data = request.get_json()
    name = data.get('name')
    tag_string = data.get('tag', '')
    if not name:
        return jsonify({'error': 'Missing name'}), 400
    tag_objs = get_or_create_tags(tag_string)
    lst = List(name=name)
    lst.tags = tag_objs
    db.session.add(lst)
    db.session.commit()
    return jsonify(serialize_list(lst)), 201

@bp.route('/api/lists/<int:list_id>', methods=['PUT'])
def api_rename_list(list_id):
    lst = List.query.get_or_404(list_id)
    data = request.get_json()
    name = data.get('name')
    if not name:
        return jsonify({'error': 'Missing name'}), 400
    lst.name = name
    db.session.commit()
    return jsonify(serialize_list(lst))

@bp.route('/api/lists/<int:list_id>', methods=['DELETE'])
def api_delete_list(list_id):
    lst = List.query.get_or_404(list_id)
    db.session.delete(lst)
    db.session.commit()
    return jsonify({'result': 'deleted'})

# ------------------ ITEMS ------------------

@bp.route('/api/lists/<int:list_id>/items', methods=['POST'])
def api_add_item(list_id):
    lst = List.query.get_or_404(list_id)
    data = request.get_json()
    text = data.get('text')
    if not text:
        return jsonify({'error': 'Missing text'}), 400
    tag = lst.tag
    # 1. Cherche la suggestion existante pour ce texte/tag
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
    return jsonify(serialize_item(item)), 201

@bp.route('/api/lists/items/<int:item_id>/toggle', methods=['PATCH'])
def api_toggle_item(item_id):
    item = Item.query.get_or_404(item_id)
    item.done = not item.done
    db.session.commit()
    return jsonify(serialize_item(item))

@bp.route('/api/lists/items/<int:item_id>', methods=['DELETE'])
def api_delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    if item.quantity > 1:
        item.quantity -= 1
        db.session.commit()
        return jsonify(serialize_item(item))
    else:
        db.session.delete(item)
        db.session.commit()
        return jsonify({'result': 'deleted'})

# ------------------ SUGGESTIONS ------------------

@bp.route('/api/lists/<int:list_id>/suggestions', methods=['GET'])
def api_get_suggestions(list_id):
    q = request.args.get('q', '')
    lst = List.query.get_or_404(list_id)
    tag = lst.tag
    # recherche insensible à la casse, max 5 résultats
    suggestions = Suggestion.query.filter(
        Suggestion.tag == tag,
        Suggestion.text.ilike(f'%{q}%')
    ).limit(5).all()
    return jsonify({'suggestions': [serialize_suggestion(s) for s in suggestions]})

@bp.route('/api/suggestions/<tag>', methods=['DELETE'])
def api_clear_suggestions(tag):
    Suggestion.query.filter_by(tag=tag).delete()
    db.session.commit()
    return jsonify({'result': 'cleared'})

