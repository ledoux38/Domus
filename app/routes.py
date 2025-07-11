from flask import Blueprint, render_template, request, redirect, url_for
from .models import db, Task, Item

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/tasks')
def all_tasks():
    tasks = Task.query.all()
    return render_template('tasks.html', tasks=tasks)


@bp.route('/task/new', methods=['POST'])
def add_task():
    name = request.form.get('name')
    if name:
        task = Task(name=name)
        db.session.add(task)
        db.session.commit()
    return redirect(url_for('main.all_tasks'))


@bp.route('/task/rename/<int:task_id>', methods=['PUT'])
def rename_task(task_id):
    name = request.form.get('name')
    task = Task.query.get_or_404(task_id)
    if name:
        task.name = name
        db.session.commit()
    return redirect(url_for('main.all_tasks'))


@bp.route('/task/<int:task_id>')
def get_task(task_id):
    task = Task.query.get_or_404(task_id)
    items = Item.query.filter_by(task_id=task.id).all()
    return render_template('task_detail.html', task=task, items=items)


@bp.route('/tasks/<int:task_id>/delete', methods=['POST'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('main.all_tasks'))


@bp.route('/tasks/<int:task_id>/add_item', methods=['POST'])
def add_item(task_id):
    text = request.form.get('text')
    if text:
        item = Item(text=text, task_id=task_id)
        db.session.add(item)
        db.session.commit()
    return redirect(url_for('main.get_task', task_id=task_id))


@bp.route('/tasks/<int:task_id>/item/<int:item_id>/toggle', methods=['POST'])
def toggle_item(task_id, item_id):
    item = Item.query.get_or_404(item_id)
    item.done = not item.done
    db.session.commit()
    return redirect(url_for('main.get_task', task_id=task_id))


@bp.route('/tasks/<int:task_id>/item/<int:item_id>/delete', methods=['POST'])
def delete_item(task_id, item_id):
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('main.get_task', task_id=task_id))
