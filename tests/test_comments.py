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

# ... [Other imports]

@pytest.fixture
def create_user_and_content(client):
    # Create a new user
    user_data = {
        "username": "test_user" + id_generator(),
        "email": "test@example.com" + id_generator(),
        "password": "password123"
    }
    user_response = client.post("/api/users", data=json.dumps(user_data), content_type="application/json")
    user_id = user_response.json["id"]

    # Create new content
    content_data = {
        "title": "Test Content",
        "description": "This is a test content",
        "file_url": "https://example.com/test.jpg",
        "content_type": "image"
    }
    access_token = create_access_token(identity=user_id)
    headers = {"Authorization": f"Bearer {access_token}"}
    content_response = client.post("/api/content", data=json.dumps(content_data), content_type="application/json", headers=headers)
    content_id = content_response.json["id"]

    return user_id, content_id, headers

def test_create_comment(client, create_user_and_content):
    user_id, content_id, headers = create_user_and_content

    # Create a new comment
    comment_data = {
        "text": "This is a test comment"
    }
    response = client.post(f"/api/content/{content_id}/comments", data=json.dumps(comment_data), content_type="application/json", headers=headers)
    assert response.status_code == 201
    assert response.json["text"] == "This is a test comment"

def test_get_comments(client, create_user_and_content):
    user_id, content_id, headers = create_user_and_content

    # Create a new comment
    comment_data = {
        "text": "This is a test comment"
    }
    response = client.post(f"/api/content/{content_id}/comments", data=json.dumps(comment_data), content_type="application/json", headers=headers)

    # Assuming a comment has already been created
    response = client.get(f"/api/content/{content_id}/comments")
    assert response.status_code == 200
    assert len(response.json) >= 1  # Checks if at least one comment is returned

def test_update_comment(client, create_user_and_content):
    user_id, content_id, headers = create_user_and_content

    # Create a new comment
    comment_data = {
        "text": "This is a test comment"
    }
    comment_response = client.post(f"/api/content/{content_id}/comments", data=json.dumps(comment_data), content_type="application/json", headers=headers)
    comment_id = comment_response.json["id"]

    # Update the comment
    update_data = {
        "text": "This is an updated test comment"
    }
    update_response = client.put(f"/api/comments/{comment_id}", data=json.dumps(update_data), content_type="application/json", headers=headers)
    assert update_response.status_code == 200
    assert update_response.json["text"] == "This is an updated test comment"

def test_delete_comment(client, create_user_and_content):
    user_id, content_id, headers = create_user_and_content

    # Create a new comment
    comment_data = {
        "text": "This is a test comment"
    }
    comment_response = client.post(f"/api/content/{content_id}/comments", data=json.dumps(comment_data), content_type="application/json", headers=headers)
    comment_id = comment_response.json["id"]

    # Delete the comment
    delete_response = client.delete(f"/api/comments/{comment_id}", headers=headers)
    assert delete_response.status_code == 200
    assert delete_response.json["message"] == "Comment deleted"
