import pytest
from rest_framework.test import APIClient
from api.models import User
from rest_framework import status
from django.contrib.auth.models import Permission

    
@pytest.fixture
def authenticated_user(db):
    user = User.objects.create_user(username='testuser', password='testpassword')
    permissions = ['add_task', 'change_task', 'delete_task']
    for permission in permissions:
        user.user_permissions.add(Permission.objects.get(codename=permission))
    
    client = APIClient()
    client.force_authenticate(user=user)
    return client, user

@pytest.mark.django_db
def test_task_view_get_all(authenticated_user):
    client, _ = authenticated_user
    response = client.get("/api/tasks/")
    
    assert response.status_code == status.HTTP_200_OK
    
    
@pytest.mark.django_db
def test_task_view_create(authenticated_user):
    client, _ = authenticated_user
    payload = {
        "name": "Task",
        "description": "Example task",
    }
    response = client.post("/api/tasks/", data=payload)
    
    assert response.status_code == status.HTTP_200_OK
    
@pytest.mark.django_db
def test_task_view_update(authenticated_user):
    client, _ = authenticated_user
    response = client.post("/api/tasks/", {"name": "Task", "description": "Example task",})
    task_id = response.data["data"]["task_id"]
    
    payload = {
        "name": "Updated Task",
        "description": "Updated Example task",
    }
    response = client.patch(f"/api/tasks/{task_id}/", data=payload)
    
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_task_view_delete(authenticated_user):
    client, _ = authenticated_user
    response = client.post("/api/tasks/", {"name": "Task", "description": "Example task",})
    task_id = response.data["data"]["task_id"]
    
    response = client.delete(f"/api/tasks/{task_id}/")
    
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_task_view_history(authenticated_user):
    client, _ = authenticated_user
    response = client.post("/api/tasks/", {"name": "Task", "description": "Example task",})
    task_id = response.data["data"]["task_id"]
    
    response = client.get(f"/api/tasks/{task_id}/history/")
    
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db 
def test_task_view_history_get_one(authenticated_user):
    client, _ = authenticated_user
    response = client.post("/api/tasks/", {"name": "Task", "description": "Example task",})
    task_id = response.data["data"]["task_id"]
    client.patch(f"/api/tasks/{task_id}/", {"name": "Updated Task", "description": "Updated Example task"})
    
    response_history = client.get(f"/api/tasks/{task_id}/history/")
    history_id = response_history.data["data"][0]["history_id"]
    
    response = client.get(f"/api/tasks/{task_id}/history/{history_id}/")
    
    assert response.status_code == status.HTTP_200_OK
 
@pytest.mark.django_db   
def test_task_view_create_not_authenticated_user():
    client = APIClient()
    
    response = client.post("/api/tasks/", {"name": "Task", "description": "Example task",})
    
    assert response.status_code == status.HTTP_403_FORBIDDEN