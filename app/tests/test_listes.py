import pytest
from app import create_app
from app.models import db, Liste

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

def test_ajout_liste(client):
    rv = client.post('/listes/nouvelle', data={'nom': 'TestListe'}, follow_redirects=True)
    assert b'TestListe' in rv.data

def test_supprime_liste(client):
    # Ajoute une liste puis la supprime
    client.post('/listes/nouvelle', data={'nom': 'TestDelete'}, follow_redirects=True)
    liste = Liste.query.filter_by(nom='TestDelete').first()
    client.post(f'/listes/{liste.id}/supprimer', follow_redirects=True)
    assert Liste.query.filter_by(nom='TestDelete').first() is None
