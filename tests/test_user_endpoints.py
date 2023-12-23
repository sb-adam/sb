import json
import pytest
from api import create_app
import config
from app import db
import string 
import random
from datetime import timedelta, datetime
from flask_jwt_extended import create_access_token
import jwt
from flask import current_app


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def generate_token(_id):
    payload = {
        'sub': _id,
        'exp': datetime.utcnow() + timedelta(days=1),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, "your-jwt-secret-key", algorithm='HS256')


@pytest.fixture
def client():
    app, jwt_manager = create_app(config.Config)
    with app.test_client() as client:
        with app.app_context():
            from api.models import User
            from api.database import Base
            db.create_all()
            print("Creating all")
            yield client
            db.drop_all()



user_id = None

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
    assert response.json['id'] is not None
    user_id = response.json['id']

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


def test_get_user(client):
    global user_id
    # Create a new user
    data = {
        "username": "test_user",
        "email": "test@example.com",
        "password": "password123"
    }
    response = client.post("/api/users", data=json.dumps(data),content_type="application/json")
    assert response.status_code == 201

    # Get the user by ID
    user_id = response.json["id"]
    access_token = create_access_token(identity=user_id)
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get(f"/api/users/{user_id}", headers=headers)
    assert response.status_code == 200
    assert response.json["username"] == "test_user"
    assert response.json["email"] == "test@example.com"

    # Test getting a nonexistent user
    response = client.get("/api/users/999", headers=headers)
    assert response.status_code == 404


def test_update_user(client):
    # Create a new user
    data = {
        "username": "test_user",
        "email": "test@example.com",
        "password": "password123"
    }
    response = client.post("/api/users", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 201
    
    # Update the user's email
    
    user_id = response.json["id"]
    access_token = create_access_token(identity=user_id)
    headers = {"Authorization": f"Bearer {access_token}"}
    data = {
        "email": "newemail@example.com"
    }
    response = client.put(f"/api/users/{user_id}", data=json.dumps(data), content_type="application/json", headers=headers)
    assert response.status_code == 200
    assert response.json["email"] == "newemail@example.com"
    
    # Update the user's username and email
    data = {
        "username": "new_username",
        "email": "newemail2@example.com"
    }
    response = client.put(f"/api/users/{user_id}", data=json.dumps(data), content_type="application/json", headers=headers)
    assert response.status_code == 200
    assert response.json["username"] == "new_username"
    assert response.json["email"] == "newemail2@example.com"

    # Try updating a different user, should fail
    data = {
        "username": "test_user2",
        "email": "test2@example.com",
        "password": "password789"
    }
    response = client.post("/api/users", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 201

    user_id2 = response.json["id"]

    updated_data2 = {
        "username": "updated_user2",
        "email": "updated2@example.com",
        "password": "password012"
    }
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.put(f"/api/users/{user_id2}", data=json.dumps(updated_data2), headers=headers, content_type="application/json")
    assert response.status_code == 401
    assert response.json["error"] == "You are not authorized to update this user's profile"
    
    # Test updating a non-existent user
    access_token = create_access_token(identity=99999)
    headers = {"Authorization": f"Bearer {access_token}"}
    data = {
        "username": "new_username",
        "email": "newemail3@example.com"
    }
    response = client.put("/api/users/99999", data=json.dumps(data), content_type="application/json", headers=headers)
    assert response.status_code == 404
