import pytest
from rest_framework.serializers import ValidationError
from api.models import Task, User
from api.serializers import UserSerializer, TaskSerializer, HistorySerializer

@pytest.fixture
def user_data():
    return {
        'username': 'testuser',
        'password': 'testpassword',
        'email': 'test@example.com',
        'first_name': 'John',
        'last_name': 'Doe',
        'phone_number': '123456789'
    }

@pytest.fixture
def task_data():
    return {
        'name': 'Test Task',
        'description': 'Description of the test task',
        'status': 'New',
        'executing_user': None 
    }


@pytest.mark.django_db
def test_user_serializer(user_data):
    serializer = UserSerializer(data=user_data)
    assert serializer.is_valid()

@pytest.mark.django_db
def test_task_serializer(task_data):
    serializer = TaskSerializer(data=task_data)
    assert serializer.is_valid()

