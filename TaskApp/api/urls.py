from django.urls import path
from .views import TaskViewSet, TaskHistoryView, UserSignUpViewSet, UserLoginViewSet, UserLogoutViewSet



urlpatterns = [
    path('register/', UserSignUpViewSet.as_view()),
    path('login/', UserLoginViewSet.as_view()),
    path('logout/', UserLogoutViewSet.as_view()),
    path('tasks/', TaskViewSet.as_view()),
    path('tasks/<int:task_id>/', TaskViewSet.as_view()),
    path('tasks/<int:task_id>/history/', TaskHistoryView.as_view()),  
    path('tasks/<int:task_id>/history/<int:history_id>/', TaskHistoryView.as_view()) 
]