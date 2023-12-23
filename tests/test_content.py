import json
import pytest
from api import create_app
import config
from app import db
from flask_jwt_extended import create_access_token
import string
import random

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

@pytest.fixture
def client():
    app, jwt_manager = create_app(config.Config)
    with app.test_client() as client:
        with app.app_context():
            from api.models import User, Content
            from api.database import Base
            db.create_all()
            yield client
            db.drop_all()

def test_create_content(client):
    # Create a new user
    data = {
        "username": "test_user",
        "email": "test@example.com",
        "password": "password123"
    }
    response = client.post("/api/users", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 201
    user_id = response.json["id"]

    # Create new content
    content_data = {
        "title": "Test Content",
        "description": "This is a test content",
        "file_url": "https://example.com/test.jpg",
        "content_type": "image"
    }

    access_token = create_access_token(identity=user_id)
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.post("/api/content", data=json.dumps(content_data), content_type="application/json", headers=headers)
    assert response.status_code == 201
    assert response.json["title"] == "Test Content"
    assert response.json["description"] == "This is a test content"

def test_get_content(client):
    # Create a new user
    data = {
        "username": "test_user",
        "email": "test@example.com",
        "password": "password123"
    }
    response = client.post("/api/users", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 201
    user_id = response.json["id"]

    # Create new content
    content_data = {
        "title": "Test Content",
        "description": "This is a test content",
        "file_url": "https://example.com/test.jpg",
        "content_type": "image"
    }

    access_token = create_access_token(identity=user_id)
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.post("/api/content", data=json.dumps(content_data), content_type="application/json", headers=headers)
    assert response.status_code == 201

    # Get all content
    response = client.get("/api/content")
    assert response.status_code == 200
    assert len(response.json) == 1

def test_update_content(client):
    # Create a new user
    data = {
        "username": "test_user",
        "email": "test@example.com",
        "password": "password123"
    }
    response = client.post("/api/users", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 201
    user_id = response.json["id"]

    # Create new content
    content_data = {
        "title": "Test Content",
        "description": "This is a test content",
        "file_url": "https://example.com/test.jpg",
        "content_type": "image"
    }

    access_token = create_access_token(identity=user_id)
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.post("/api/content", data=json.dumps(content_data), content_type="application/json", headers=headers)
    assert response.status_code == 201

    content_id = response.json["id"]
    new_content_data = {
        "title": "Updated Content",
        "description": "This is an updated test content",
        "file_url": "https://example.com/updated.jpg"
    }

    response = client.put(f"/api/content/{content_id}", data=json.dumps(new_content_data), content_type="application/json", headers=headers)
    assert response.status_code == 200
    assert response.json["title"] == "Updated Content"
    assert response.json["description"] == "This is an updated test content"

def test_delete_content(client):
    # Create a new user
    data = {
        "username": "test_user",
        "email": "test@example.com",
        "password": "password123"
    }
    response = client.post("/api/users", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 201
    user_id = response.json["id"]

    # Create new content
    content_data = {
        "title": "Test Content",
        "description": "This is a test content",
        "file_url": "https://example.com/test.jpg",
        "content_type": "image"
    }

    access_token = create_access_token(identity=user_id)
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.post("/api/content", data=json.dumps(content_data), content_type="application/json", headers=headers)
    assert response.status_code == 201

    content_id = response.json["id"]

    # Delete content
    response = client.delete(f"/api/content/{content_id}", headers=headers)
    assert response.status_code == 200
    assert response.json["message"] == "Content deleted"
