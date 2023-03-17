import json
import pytest
from api.app import create_app
from api.models import db, User


@pytest.fixture
def client():
    app = create_app("test")
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()


def test_create_user(client):
    # Test successful user creation
    data = {
        "username": "test_user",
        "email": "test@example.com",
        "password": "password123"
    }
    response = client.post("/users", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 201
    assert response.json["username"] == "test_user"
    assert response.json["email"] == "test@example.com"

    # Test duplicate email
    data = {
        "username": "test_user2",
        "email": "test@example.com",
        "password": "password456"
    }
    response = client.post("/users", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 400
    assert response.json["error"] == "User with this email or username already exists"

    # Test duplicate username
    data = {
        "username": "test_user",
        "email": "test2@example.com",
        "password": "password789"
    }
    response = client.post("/users", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 400
    assert response.json["error"] == "User with this email or username already exists"
