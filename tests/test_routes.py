import pytest
from app import create_app, db
from app.models import User

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

def test_register(client):
    response = client.post('/register', json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123"
    })
    assert response.status_code == 201

def test_get_user(client):
    user = User(username="testuser", email="test@example.com", password="password123")
    db.session.add(user)
    db.session.commit()

    response = client.get(f'/users/{user.id}')
    assert response.status_code == 200
    assert response.json['username'] == "testuser"

def test_update_user(client):
    user = User(username="testuser", email="test@example.com", password="password123")
    db.session.add(user)
    db.session.commit()

    response = client.put(f'/users/{user.id}', json={"username": "updateduser"})
    assert response.status_code == 200
    assert User.query.get(user.id).username == "updateduser"

def test_delete_user(client):
    user = User(username="testuser", email="test@example.com", password="password123")
    db.session.add(user)
    db.session.commit()

    response = client.delete(f'/users/{user.id}')
    assert response.status_code == 200
    assert User.query.get(user.id) is None
