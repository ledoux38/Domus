import pytest
from app import create_app
from app.models import db, List, Suggestion, Item


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
    response = client.post('/list/new', data={'name': 'MaListe', 'tag': 'courses'}, follow_redirects=True)
    assert b'MaListe' in response.data
    lst = List.query.filter_by(name='MaListe', tag='courses').first()
    assert lst is not None


def test_add_item_and_create_suggestion(client):
    # Ajout liste
    client.post('/list/new', data={'name': 'Courses', 'tag': 'groceries'}, follow_redirects=True)
    lst = List.query.filter_by(name='Courses').first()
    # Ajout premier item (nouvelle suggestion)
    client.post(f'/lists/{lst.id}/add_item', data={'text': 'Lait'}, follow_redirects=True)
    suggestion = Suggestion.query.filter_by(text='Lait', tag='groceries').first()
    assert suggestion is not None
    item = Item.query.filter_by(list_id=lst.id, suggestion_id=suggestion.id).first()
    assert item is not None
    assert item.quantity == 1


def test_add_existing_item_increments_quantity(client):
    client.post('/list/new', data={'name': 'Courses', 'tag': 'groceries'}, follow_redirects=True)
    lst = List.query.filter_by(name='Courses').first()
    client.post(f'/lists/{lst.id}/add_item', data={'text': 'Lait'}, follow_redirects=True)
    client.post(f'/lists/{lst.id}/add_item', data={'text': 'Lait'}, follow_redirects=True)
    suggestion = Suggestion.query.filter_by(text='Lait', tag='groceries').first()
    item = Item.query.filter_by(list_id=lst.id, suggestion_id=suggestion.id).first()
    assert item.quantity == 2


def test_delete_item_decrements_or_removes(client):
    client.post('/list/new', data={'name': 'Courses', 'tag': 'groceries'}, follow_redirects=True)
    lst = List.query.filter_by(name='Courses').first()
    client.post(f'/lists/{lst.id}/add_item', data={'text': 'Bacon'}, follow_redirects=True)
    client.post(f'/lists/{lst.id}/add_item', data={'text': 'Bacon'}, follow_redirects=True)
    suggestion = Suggestion.query.filter_by(text='Bacon', tag='groceries').first()
    item = Item.query.filter_by(list_id=lst.id, suggestion_id=suggestion.id).first()
    assert item.quantity == 2

    # Premier delete (quantity - 1)
    client.post(f'/lists/{lst.id}/item/{item.id}/delete', follow_redirects=True)
    item = Item.query.filter_by(list_id=lst.id, suggestion_id=suggestion.id).first()
    assert item.quantity == 1

    # Second delete (item supprimé)
    client.post(f'/lists/{lst.id}/item/{item.id}/delete', follow_redirects=True)
    item = Item.query.filter_by(list_id=lst.id, suggestion_id=suggestion.id).first()
    assert item is None


def test_suggestion_persists_after_item_and_list_deletion(client):
    client.post('/list/new', data={'name': 'Courses', 'tag': 'groceries'}, follow_redirects=True)
    lst = List.query.filter_by(name='Courses').first()
    client.post(f'/lists/{lst.id}/add_item', data={'text': 'Oeufs'}, follow_redirects=True)
    suggestion = Suggestion.query.filter_by(text='Oeufs', tag='groceries').first()
    item = Item.query.filter_by(list_id=lst.id, suggestion_id=suggestion.id).first()
    # Suppression de l'item
    client.post(f'/lists/{lst.id}/item/{item.id}/delete', follow_redirects=True)
    # Suppression de la liste
    client.post(f'/lists/{lst.id}/delete', follow_redirects=True)
    # La suggestion existe toujours
    suggestion = Suggestion.query.filter_by(text='Oeufs', tag='groceries').first()
    assert suggestion is not None


def test_suggestions_search(client):
    client.post('/list/new', data={'name': 'Courses', 'tag': 'groceries'}, follow_redirects=True)
    lst = List.query.filter_by(name='Courses').first()
    for text in ['Lait', 'Oeufs', 'Bacon', 'Jambon', 'Beurre', 'Pain']:
        client.post(f'/lists/{lst.id}/add_item', data={'text': text}, follow_redirects=True)
    # Recherche suggestions avec "a" (doit retourner max 5 résultats)
    response = client.get(f'/lists/{lst.id}/suggestions?q=a')
    data = response.get_json()
    assert 'suggestions' in data
    assert len(data['suggestions']) <= 5
    assert any('a' in s.lower() for s in data['suggestions'])
