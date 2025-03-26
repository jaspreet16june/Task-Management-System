from rest_framework import viewsets, status
from .models import Task, User
from .serializers import TaskSerializer, UserSerializer
from rest_framework.decorators import action
from rest_framework.response import Response



class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    
    def get_queryset(self):
        user_id = self.request.query_params.get('user_id', None)
        if user_id:
            return Task.objects.filter(assigned_users__id=user_id)
        return Task.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        task = serializer.save()
          
        return Response(
            {"message": "Task created successfully", "task_id": task.id},
            status=status.HTTP_201_CREATED
        )
    
    def update(self, request, *args, **kwargs):
        pk = kwargs.pop('pk','')
        try:
            instance = Task.objects.get(id=pk)
        except Task.DoesNotExist:
            return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(instance, data=request.data, partial=None)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer) 

        return Response(
            {"message": "Task updated successfully", "task_id": instance.id},
            status=status.HTTP_200_OK
        )
    
    
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    