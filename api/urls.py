from django.urls import path
from .views import TaskViewSet, TaskHistoryView, UserSignUpViewSet

#tu są patterny skrótów hhtp endpointów

urlpatterns = [
    path('register/', UserSignUpViewSet.as_view()),
    #path('login/', UserLoginView.as_view(), name='user-login'),
    path('tasks/', TaskViewSet.as_view()),
    path('tasks/<int:task_id>/', TaskViewSet.as_view()),
    path('tasks/<int:task_id>/history/', TaskHistoryView.as_view()),  
    path('tasks/<int:task_id>/history/<int:history_id>/', TaskHistoryView.as_view()) 
]