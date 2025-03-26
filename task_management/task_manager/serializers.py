from datetime import datetime
from rest_framework import serializers
from .models import User, Task


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    Handles serialization and deserialization of User objects.
    """
    class Meta:
        model = User
        fields = ['name', 'email', 'mobile_no', 'created_at', 'modified_at']
        
            
class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for the Task model.
    Handles serialization, deserialization, creation, and updating of Task objects.
    """
    name = serializers.CharField(required=False)

    # Allows assigning multiple users to a task (many-to-many relationship)
    assigned_users = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(),many=True, required=False, allow_empty=True)
    
    def create(self, validated_data):  
        """
        Create a new Task instance.

        Removes 'assigned_users' from validated data, creates the task,
        and sets the assigned users.

        Args:
            validated_data (dict): Validated data for the new Task.

        Returns:
            Task: The newly created Task instance.
        """      
        assigned_users = validated_data.pop('assigned_users', [])  
        task = Task.objects.create(**validated_data)  
        task.assigned_users.set(assigned_users)  
        return task

    def update(self, instance, validated_data):
        """
        Update an existing Task instance.

        Prevents modification of a completed task.
        Updates the task status and assigned users if provided.

        Args:
            instance (Task): The existing Task instance to be updated.
            validated_data (dict): Data for updating the Task.

        Returns:
            Task: The updated Task instance.

        Raises:
            serializers.ValidationError: If attempting to update a completed task.
        """
        
        if instance.status == 'completed':
            raise serializers.ValidationError({"error": "Cannot update a completed task."})

        if 'status' in validated_data:
            instance.status = validated_data['status']
            if  validated_data['status'] == 'completed':
                instance.completed_at = datetime.now()
                
        if 'assigned_users' in validated_data:
            instance.assigned_users.set(validated_data['assigned_users'])
        instance.save()
        return instance

    class Meta:
        model = Task
        fields = ['name','description', 'task_type', 'status', 'completed_at', 'assigned_users']
        