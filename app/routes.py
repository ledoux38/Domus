from flask import Blueprint, render_template, request, redirect, url_for

from .models import db, List, Suggestion, Item

bp = Blueprint('main', __name__)


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
    tag = request.form.get('tag')
    if name and tag:
        list_ = List(name=name, tag=tag)
        db.session.add(list_)
        db.session.commit()
    return redirect(url_for('main.all_lists'))


@bp.route('/list/rename/<int:list_id>', methods=['PUT'])
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
    tag = list_.tag

    suggestion = Suggestion.query.filter(
        db.func.lower(Suggestion.text) == text.lower(),
        Suggestion.tag == tag
    ).first()

    if not suggestion:
        suggestion = Suggestion(text=text, tag=tag)
        db.session.add(suggestion)
        db.session.commit()

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
    tag = list_.tag
    suggestions = Suggestion.query.filter(
        Suggestion.tag == tag,
        Suggestion.text.ilike(f'%{q}%')
    ).limit(5).all()

    return {'suggestions': [s.text for s in suggestions]}


@bp.route('/suggestions/<tag>/clear', methods=['POST'])
def clear_suggestions(tag):
    Suggestion.query.filter_by(tag=tag).delete()
    db.session.commit()
    return redirect(url_for('main.all_lists'))


@bp.route('/tags/suggestions')
def tag_suggestions():
    q = request.args.get('q', '')
    tags = (
        db.session.query(List.tag)
        .filter(List.tag.ilike(f'%{q}%'))
        .distinct()
        .limit(5)
        .all()
    )
    return {'suggestions': [t[0] for t in tags if t[0]]}