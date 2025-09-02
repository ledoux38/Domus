import pytest
from app import create_app
from app.models import db, List, Suggestion, Item, Tag


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


def get_tag(name):
    """Récupère (ou crée) un tag avec le nom donné."""
    tag = Tag.query.filter_by(name=name).first()
    if not tag:
        tag = Tag(name=name)
        db.session.add(tag)
        db.session.commit()
    return tag


def get_list_by_name_and_tag(name, tag_name):
    tag = get_tag(tag_name)
    return List.query.filter(
        List.name == name,
        List.tags.any(Tag.name == tag.name)
    ).first()


def get_suggestion_by_text_and_tag(text, tag_name):
    tag = get_tag(tag_name)
    return Suggestion.query.filter(
        Suggestion.text == text,
        Suggestion.tags.any(Tag.name == tag.name)
    ).first()


def test_add_list(client):
    # Ajoute une liste avec tag "courses"
    response = client.post('/list/new', data={'name': 'MaListe', 'tags': 'courses'}, follow_redirects=True)
    assert b'MaListe' in response.data
    lst = get_list_by_name_and_tag('MaListe', 'courses')
    assert lst is not None


def test_add_list_no_tag(client):
    # Ajoute une liste sans tag (doit créer le tag "indefinie")
    response = client.post('/list/new', data={'name': 'Liste sans tag'}, follow_redirects=True)
    lst = get_list_by_name_and_tag('Liste sans tag', 'indefinie')
    assert lst is not None


def test_add_item_and_create_suggestion(client):
    # Ajout liste avec tag groceries
    client.post('/list/new', data={'name': 'Courses', 'tags': 'groceries'}, follow_redirects=True)
    lst = get_list_by_name_and_tag('Courses', 'groceries')
    # Ajout item (nouvelle suggestion)
    client.post(f'/lists/{lst.id}/add_item', data={'text': 'Lait'}, follow_redirects=True)
    suggestion = get_suggestion_by_text_and_tag('Lait', 'groceries')
    item = Item.query.filter_by(list_id=lst.id, suggestion_id=suggestion.id).first()
    assert suggestion is not None
    assert item is not None
    assert item.quantity == 1


def test_add_existing_item_increments_quantity(client):
    client.post('/list/new', data={'name': 'Courses', 'tags': 'groceries'}, follow_redirects=True)
    lst = get_list_by_name_and_tag('Courses', 'groceries')
    client.post(f'/lists/{lst.id}/add_item', data={'text': 'Lait'}, follow_redirects=True)
    client.post(f'/lists/{lst.id}/add_item', data={'text': 'Lait'}, follow_redirects=True)
    suggestion = get_suggestion_by_text_and_tag('Lait', 'groceries')
    item = Item.query.filter_by(list_id=lst.id, suggestion_id=suggestion.id).first()
    assert item.quantity == 2


def test_delete_item_decrements_or_removes(client):
    client.post('/list/new', data={'name': 'Courses', 'tags': 'groceries'}, follow_redirects=True)
    lst = get_list_by_name_and_tag('Courses', 'groceries')
    client.post(f'/lists/{lst.id}/add_item', data={'text': 'Bacon'}, follow_redirects=True)
    client.post(f'/lists/{lst.id}/add_item', data={'text': 'Bacon'}, follow_redirects=True)
    suggestion = get_suggestion_by_text_and_tag('Bacon', 'groceries')
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
    client.post('/list/new', data={'name': 'Courses', 'tags': 'groceries'}, follow_redirects=True)
    lst = get_list_by_name_and_tag('Courses', 'groceries')
    client.post(f'/lists/{lst.id}/add_item', data={'text': 'Oeufs'}, follow_redirects=True)
    suggestion = get_suggestion_by_text_and_tag('Oeufs', 'groceries')
    item = Item.query.filter_by(list_id=lst.id, suggestion_id=suggestion.id).first()
    # Suppression de l'item
    client.post(f'/lists/{lst.id}/item/{item.id}/delete', follow_redirects=True)
    # Suppression de la liste
    client.post(f'/lists/{lst.id}/delete', follow_redirects=True)
    # La suggestion existe toujours, liée à "groceries"
    suggestion = get_suggestion_by_text_and_tag('Oeufs', 'groceries')
    assert suggestion is not None


def test_suggestions_search(client):
    client.post('/list/new', data={'name': 'Courses', 'tags': 'groceries'}, follow_redirects=True)
    lst = get_list_by_name_and_tag('Courses', 'groceries')
    for text in ['Lait', 'Oeufs', 'Bacon', 'Jambon', 'Beurre', 'Pain']:
        client.post(f'/lists/{lst.id}/add_item', data={'text': text}, follow_redirects=True)
    # Recherche suggestions avec "a" et filtrage par tag "groceries" (max 5 résultats)
    response = client.get(f'/lists/{lst.id}/suggestions?q=a&tag=groceries')
    data = response.get_json()
    assert 'suggestions' in data
    assert len(data['suggestions']) <= 5
    assert all('groceries' in s['tags'] for s in data['suggestions'])
    assert any('a' in s['text'].lower() for s in data['suggestions'])


def test_tag_suggestions_api(client):
    client.post('/list/new', data={'name': 'Courses', 'tags': 'groceries'}, follow_redirects=True)
    client.post('/list/new', data={'name': 'Travail', 'tags': 'bureau'}, follow_redirects=True)
    response = client.get('/api/tags/suggestions?q=gro')
    data = response.get_json()
    assert 'suggestions' in data
    assert 'groceries' in data['suggestions']
