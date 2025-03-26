from rest_framework import viewsets, status
from .models import Task, User
from .serializers import TaskSerializer, UserSerializer
from rest_framework.decorators import action
from rest_framework.response import Response



class TaskViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows tasks to be viewed, created, updated, or deleted.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    
    def get_queryset(self):
        """
        Retrieve a list of tasks. If `user_id` is provided as a query parameter, 
        it filters tasks assigned to that specific user.
        
        Query Parameters:
        - user_id (optional): Filter tasks assigned to a specific user.

        Returns:
        - List of Task objects.
        """
        user_id = self.request.query_params.get('user_id', None)
        if user_id:
            return Task.objects.filter(assigned_users__id=user_id)
        return Task.objects.all()

    def create(self, request, *args, **kwargs):
        """
        Create a new task.
        
        Request Body:
        - Required fields for creating a task (defined in TaskSerializer).

        Returns:
        - Success message with task ID if creation is successful.
        - 400 Bad Request if the request data is invalid.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        task = serializer.save()
          
        return Response(
            {"message": "Task created successfully", "task_id": task.id},
            status=status.HTTP_201_CREATED
        )
    
    def update(self, request, *args, **kwargs):
        """
        Update an existing task.

        URL Parameters:
        - pk (int): Task ID to be updated.

        Request Body:
        - Fields to be updated (defined in TaskSerializer).

        Returns:
        - Success message with task ID if update is successful.
        - 404 Not Found if the task does not exist.
        - 400 Bad Request if request data is invalid.
        """
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
    """
    API endpoint that allows users to be viewed, created, updated, or deleted.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    