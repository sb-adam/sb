import json
import pytest
from api import create_app
import config
from app import db
import string 
import random

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


@pytest.fixture
def client():
    app = create_app(config.Config)
    with app.test_client() as client:
        with app.app_context():
            from api.models import User
            from api.database import Base
            db.create_all()
            print("Creating all")
            yield client
            db.drop_all()


def test_create_user(client):
    # Test successful user creation
    name = "test_user" + id_generator()
    email = "test@example.com" + id_generator()
    data = {
        "username": name,
        "email": email,
        "password": "password123"
    }
    response = client.post("/api/users", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 201
    assert response.json["username"] == name
    assert response.json["email"] == email

    # Test duplicate email
    data = {
        "username": "test_user" + id_generator(),
        "email": email,
        "password": "password456"
    }
    response = client.post("/api/users", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 400
    assert response.json["error"] == "User with this email or username already exists"

    # # Test duplicate username
    data = {
        "username": name,
        "email": "test2@example.com",
        "password": "password789"
    }
    response = client.post("/api/users", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 400
    assert response.json["error"] == "User with this email or username already exists"
