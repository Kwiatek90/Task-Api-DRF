from django.db import models
from django.contrib.auth.models import AbstractUser
from simple_history.models import HistoricalRecords
from django.utils import timezone

class User(AbstractUser):
    phone_number = models.CharField(blank=True, max_length=15, null=True)
    
class Task(models.Model):
    task_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, blank=False, null=False)
    description = models.TextField(max_length=255, blank=True, null=True)
    status_choices = [('New', 'New'), ('In progress', 'In progress'), ('Completed', 'Completed')]
    status = models.CharField(max_length=20, choices=status_choices, default='New')
    executing_user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)#tu zmienic z id na username
    history = HistoricalRecords()
    
    @property
    def _history_date(self):
        return self.__history_date
    
    @_history_date.setter
    def _history_date(self, value):
        self.__history_date = timezone.localtime(value)
    
