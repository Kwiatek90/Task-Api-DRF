from django.shortcuts import get_object_or_404
from . import models, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from datetime import datetime
from django.utils import timezone


class TaskViewSet(APIView):
    
    def get(self, request ,task_id=None):
        '''Wyświetlanie rekordu lub wszytskich rekordów'''
        if task_id:
            item = models.Task.objects.get(task_id=task_id)
            serializer = serializers.TaskSerializer(item)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        
        user_id = request.query_params.get('user_id')   
        task_status = request.query_params.get('status')
        keyword = request.query_params.get('keyword')
        
        query = models.Task.objects.all()    
            
        if user_id:
            query = query.filter(executing_user=user_id)
        if task_status:
            query = query.filter(status=task_status)
        if keyword:
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
            return Response({"status": "success", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
    def patch(self, request, task_id=None):
        '''Edycja rekordów''' 
        item = models.Task.objects.get(task_id=task_id)
        serializer = serializers.TaskSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "success", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, task_id=None):
        item = models.Task.objects.filter(task_id=task_id)
        item.delete()
        return Response({"status": "success", "data": "Item Deleted"})
    
class TaskHistoryView(APIView):
    
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
        


