import pytest
from rest_framework.test import APIClient
from api.models import User

client = APIClient()

@pytest.fixture
def authenticated_user(db):
    user = User.objects.create_user(username='testuser', password='testpassword')
    client = APIClient()
    client.force_authenticate(user=user)
    return client, user

@pytest.mark.django_db
def test_register_user():
    payload = {
        "username": "TestUser",
        "password": "TestUser",
        "email": "testuser@gmail.com",
        "first_name": "user",
        "last_name": "UserLastName",
        "phone_number": 567890123 
    }
    
    response = client.post("/api/register/", payload)
    data = response.data
    
    assert data["status"]== "success"
    assert data["data"]["username"] == payload["username"]
    assert data["data"]["email"] == payload["email"]
    assert data["data"]["first_name"] == payload["first_name"]
    assert data["data"]["last_name"] == payload["last_name"]
    assert data["data"]["last_name"] == f"{payload['last_name']}"
    assert "password" not in data
  
@pytest.mark.django_db    
def test_register_user_fail():
    payload = {
        "password": "TestUser",
        "email": "testuser@gmail.com",
        "first_name": "user",
        "last_name": "UserLastName",
        "phone_number": 567890123 
    }
    
    response = client.post("/api/register/", payload)
    data = response.data
    
    assert data["status"]== "failed"

@pytest.mark.django_db    
def test_login_user():
    payload = {
        "username": "TestUser",
        "password": "TestUser",
        "email": "testuser@gmail.com",
        "first_name": "user",
        "last_name": "UserLastName",
        "phone_number": 567890123 
    }
    
    client.post("/api/register/", payload)
    
    
    log_dict = {"username": "TestUser", "password": "TestUser"}
    
    response = client.post("/api/login/", log_dict)
   
    
    assert response.status_code == 200
    
@pytest.mark.django_db    
def test_login_user_fail():
    payload = {
        "username": "TestUser",
        "password": "TestUser",
        "email": "testuser@gmail.com",
        "first_name": "user",
        "last_name": "UserLastName",
        "phone_number": 567890123 
    }
    
    client.post("/api/register/", payload)
    
    
    log_dict = {"username": "TestUsera", "password": "TestUser"}
    
    response = client.post("/api/login/", log_dict)
    data = response.data
    
    assert data["Status"] == "failed"

    
    
