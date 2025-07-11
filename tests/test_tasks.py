import pytest
from app import create_app
from app.models import db, Task, Item

@pytest.fixture
def client():
    test_config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
    }
    app = create_app(test_config)
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

def test_add_task(client):
    response = client.post('/tasks/new', data={'nom': 'MaListe'}, follow_redirects=True)
    assert b'MaListe' in response.data

def test_add_item(client):
    client.post('/tasks/new', data={'name': 'Courses'}, follow_redirects=True)
    task = Task.query.filter_by(name='Courses').first()
    client.post(f'/tasks/{task.id}/add_item', data={'text': 'Lait'}, follow_redirects=True)
    assert Item.query.filter_by(task_id=task.id, text='Lait').first() is not None

def test_toggle_item(client):
    client.post('/tasks/new', data={'name': 'Courses'}, follow_redirects=True)
    task = Task.query.filter_by(name='Courses').first()
    client.post(f'/tasks/{task.id}/add_item', data={'text': 'Pain'}, follow_redirects=True)
    item = Item.query.filter_by(task_id=task.id, text='Pain').first()
    assert not item.done
    client.post(f'/tasks/{task.id}/item/{item.id}/toggle', follow_redirects=True)
    item = Item.query.get(item.id)
    assert item.done

def test_rename_task(client):
    client.post('/tasks/new', data={'name': 'AncienNom'}, follow_redirects=True)
    task = Task.query.filter_by(name='AncienNom').first()
    client.post(f'/tasks/{task.id}', data={'name': 'NouveauNom'}, follow_redirects=True)
    task = Task.query.get(task.id)
    assert task.name == 'NouveauNom'

def test_delete_item(client):
    client.post('/tasks/new', data={'name': 'Courses'}, follow_redirects=True)
    task = Task.query.filter_by(name='Courses').first()
    client.post(f'/tasks/{task.id}/add_item', data={'text': 'Oeufs'}, follow_redirects=True)
    item = Item.query.filter_by(task_id=task.id, text='Oeufs').first()
    client.post(f'/tasks/{task.id}/item/{item.id}/delete', follow_redirects=True)
    assert Item.query.get(item.id) is None

def test_delete_task(client):
    client.post('/tasks/new', data={'name': 'À supprimer'}, follow_redirects=True)
    task = Task.query.filter_by(name='À supprimer').first()
    client.post(f'/tasks/{task.id}/delete', follow_redirects=True)
    assert Task.query.get(task.id) is None
