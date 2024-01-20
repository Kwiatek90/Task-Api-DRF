from . import models, serializers

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from datetime import datetime
from django.utils import timezone
from django.contrib.auth import authenticate, login
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.authtoken.models import Token

class TaskViewSet(APIView):
    queryset = models.Task.objects.all()
    authentication_classes = [SessionAuthentication]
    permission_classes = [DjangoModelPermissions]
    
    def get(self, request ,task_id=None):
        '''Wyświetlanie rekordu lub wszytskich rekordów'''
        if task_id:
            item = models.Task.objects.get(task_id=task_id)
            serializer = serializers.TaskSerializer(item)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        
        executing_user = request.query_params.get('executing_user')   
        task_status = request.query_params.get('status')
        keyword = request.query_params.get('keyword')
        
        query = models.Task.objects.all()    
            
        if executing_user:
            query = query.filter(executing_user=executing_user)
        elif task_status:
            query = query.filter(status=task_status)
        elif keyword:
            query = query.filter(Q(name__icontains=keyword) | Q(description__icontains=keyword))
        else:
            query = models.Task.objects.all()    
            
        serializer = serializers.TaskSerializer(query, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
    
    def post(self, request):
        '''Tworzenie rekordów'''
        serializer = serializers.TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "failed", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
    def patch(self, request, task_id=None):
        '''Edycja rekordów''' 
        item = models.Task.objects.get(task_id=task_id)
        serializer = serializers.TaskSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "failed", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, task_id=None):
        item = models.Task.objects.filter(task_id=task_id)
        item.delete()
        return Response({"status": "success", "data": "Item Deleted"})
    
class TaskHistoryView(APIView):
    queryset = models.Task.objects.all()
    authentication_classes = [SessionAuthentication]
    permission_classes = [DjangoModelPermissions]
    
    def get(self, request, task_id=None, history_id=None):
        '''Pobieranie historii zmian dla zadań'''
        task = models.Task.objects.get(task_id=task_id)
        
        if history_id:
            snapshot = task.history.get(history_id=history_id)
            serializer = serializers.HistorySerializer(snapshot)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        
        start_date_str = request.query_params.get('start_date')
        end_date_str = request.query_params.get('end_date')
        executing_user = request.query_params.get('executing_user') 
    
        history = task.history.all()
        
        if start_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            start_date_aware = timezone.make_aware(start_date, timezone.get_default_timezone())
            history = history.filter(history_date__gte=start_date_aware)

        if end_date_str:
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
            end_date_aware = timezone.make_aware(end_date, timezone.get_default_timezone())
            history = history.filter(history_date__lte=end_date_aware)
            
        if executing_user:
            if executing_user.isdigit():
                history = history.filter(executing_user__id=executing_user)
            else:
                history = history.filter(Q(executing_user__username=executing_user) | Q(executing_user__isnull=True))

        serializer = serializers.HistorySerializer(history, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        
class UserSignUpViewSet(APIView):
    
    def post(self, request):
        serializer = serializers.UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = models.User.objects.get(username=request.data['username'])
            user.set_password(request.data['password'])
            user.save()
            token = Token.objects.create(user=user)
            return Response({"status": "success", 'token': token.key, "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"status": "failed", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
class UserLoginViewSet(APIView):
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({"Status": "success", 'token': token.key, "data": serializers.UserSerializer(user).data}, status=status.HTTP_200_OK)
        else:
            return Response({"Status": "failed", "data": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        
class UserLogoutViewSet(APIView):
    
    authentication_classes = [SessionAuthentication]
    
    def post(self, request):
        try:
            print(request.user)
            request.user.auth_token.delete()
            return Response({"Status": "success", 'Message': 'Successfully logged out.',}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"Status": "failed", "Error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)