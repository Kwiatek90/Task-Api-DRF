from rest_framework import serializers
from .models import Task, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name', 'phone_number')
        extra_kwargs = {'password': {'write_only': True}}
        
class TaskSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Task
        fields = ('task_id', 'name', 'description', 'status', 'executing_user')
        
class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Task.history.model
        fields = ('history_id','task_id', 'name', 'description', 'status', 'executing_user', 'history_date', 'history_user')
        
        
