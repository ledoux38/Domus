import pytest
from app import create_app
from app.models import db, Liste, Item

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

def test_ajout_liste(client):
    response = client.post('/listes/nouvelle', data={'nom': 'MaListe'}, follow_redirects=True)
    assert b'MaListe' in response.data

def test_ajout_item(client):
    client.post('/listes/nouvelle', data={'nom': 'Courses'}, follow_redirects=True)
    liste = Liste.query.filter_by(nom='Courses').first()
    client.post(f'/listes/{liste.id}/ajouter_item', data={'texte': 'Lait'}, follow_redirects=True)
    assert Item.query.filter_by(liste_id=liste.id, texte='Lait').first() is not None

def test_toggle_item(client):
    client.post('/listes/nouvelle', data={'nom': 'Courses'}, follow_redirects=True)
    liste = Liste.query.filter_by(nom='Courses').first()
    client.post(f'/listes/{liste.id}/ajouter_item', data={'texte': 'Pain'}, follow_redirects=True)
    item = Item.query.filter_by(liste_id=liste.id, texte='Pain').first()
    assert not item.fait
    client.post(f'/listes/{liste.id}/item/{item.id}/toggle', follow_redirects=True)
    item = Item.query.get(item.id)
    assert item.fait

def test_renomme_liste(client):
    client.post('/listes/nouvelle', data={'nom': 'AncienNom'}, follow_redirects=True)
    liste = Liste.query.filter_by(nom='AncienNom').first()
    client.post(f'/listes/{liste.id}', data={'nom': 'NouveauNom'}, follow_redirects=True)
    liste = Liste.query.get(liste.id)
    assert liste.nom == 'NouveauNom'

def test_supprimer_item(client):
    client.post('/listes/nouvelle', data={'nom': 'Courses'}, follow_redirects=True)
    liste = Liste.query.filter_by(nom='Courses').first()
    client.post(f'/listes/{liste.id}/ajouter_item', data={'texte': 'Oeufs'}, follow_redirects=True)
    item = Item.query.filter_by(liste_id=liste.id, texte='Oeufs').first()
    client.post(f'/listes/{liste.id}/item/{item.id}/supprimer', follow_redirects=True)
    assert Item.query.get(item.id) is None

def test_supprimer_liste(client):
    client.post('/listes/nouvelle', data={'nom': 'À supprimer'}, follow_redirects=True)
    liste = Liste.query.filter_by(nom='À supprimer').first()
    client.post(f'/listes/{liste.id}/supprimer', follow_redirects=True)
    assert Liste.query.get(liste.id) is None
