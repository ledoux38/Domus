from flask import Blueprint, render_template, request, redirect, url_for
from .models import db, List, Item

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
    if name:
        list = List(name=name)
        db.session.add(list)
        db.session.commit()
    return redirect(url_for('main.all_lists'))


@bp.route('/list/rename/<int:list_id>', methods=['PUT'])
def rename_list(list_id):
    name = request.form.get('name')
    list = List.query.get_or_404(list_id)
    if name:
        list.name = name
        db.session.commit()
    return redirect(url_for('main.all_lists'))


@bp.route('/list/<int:list_id>')
def get_list(list_id):
    list = List.query.get_or_404(list_id)
    items = Item.query.filter_by(list_id=list.id).all()
    return render_template('list_detail.html', list=list, items=items)


@bp.route('/lists/<int:list_id>/delete', methods=['POST'])
def delete_list(list_id):
    list = List.query.get_or_404(list_id)
    db.session.delete(list)
    db.session.commit()
    return redirect(url_for('main.all_lists'))


@bp.route('/lists/<int:list_id>/add_item', methods=['POST'])
def add_item(list_id):
    text = request.form.get('text')
    if text:
        item = Item(text=text, list_id=list_id)
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
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('main.get_list', list_id=list_id))
