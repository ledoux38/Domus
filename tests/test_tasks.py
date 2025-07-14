import pytest
from app import create_app
from app.models import db, List, Item

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

def test_add_list(client):
    response = client.post('/list/new', data={'name': 'MaListe'}, follow_redirects=True)
    assert b'MaListe' in response.data

def test_add_item(client):
    client.post('/list/new', data={'name': 'Courses'}, follow_redirects=True)
    list = List.query.filter_by(name='Courses').first()
    client.post(f'/list/{list.id}/add_item', data={'text': 'Lait'}, follow_redirects=True)
    o = Item.query.filter_by(list_id=list.id, text='Lait').first()
    assert o is not None

def test_toggle_item(client):
    client.post('/list/new', data={'name': 'Courses'}, follow_redirects=True)
    list = List.query.filter_by(name='Courses').first()
    client.post(f'/lists/{list.id}/add_item', data={'text': 'Pain'}, follow_redirects=True)
    item = Item.query.filter_by(list_id=list.id, text='Pain').first()
    assert not item.done
    client.post(f'/lists/{list.id}/item/{item.id}/toggle', follow_redirects=True)
    item = Item.query.get(item.id)
    assert item.done

def test_rename_list(client):
    client.post('/list/new', data={'name': 'AncienNom'}, follow_redirects=True)
    list = List.query.filter_by(name='AncienNom').first()
    client.put(f'/list/rename/{list.id}', data={'name': 'NouveauNom'}, follow_redirects=True)
    list = List.query.get(list.id)
    assert list.name == 'NouveauNom'

def test_delete_item(client):
    client.post('/list/new', data={'name': 'Courses'}, follow_redirects=True)
    list = List.query.filter_by(name='Courses').first()
    client.post(f'/lists/{list.id}/add_item', data={'text': 'Oeufs'}, follow_redirects=True)
    item = Item.query.filter_by(list_id=list.id, text='Oeufs').first()
    client.post(f'/lists/{list.id}/item/{item.id}/delete', follow_redirects=True)
    assert Item.query.get(item.id) is None

def test_delete_list(client):
    client.post('/list/new', data={'name': 'À supprimer'}, follow_redirects=True)
    list = List.query.filter_by(name='À supprimer').first()
    client.post(f'/lists/{list.id}/delete', follow_redirects=True)
    assert List.query.get(list.id) is None
