from django.urls import path
from .views import TaskViewSet, TaskHistoryView

#tu są patterny skrótów hhtp endpointów

urlpatterns = [
    path('tasks/', TaskViewSet.as_view()),
    path('tasks/<int:task_id>/', TaskViewSet.as_view()),
    path('tasks/<int:task_id>/history/', TaskHistoryView.as_view()),  
    path('tasks/<int:task_id>/history/<int:history_id>/', TaskHistoryView.as_view()) 
]