from datetime import datetime
from rest_framework import serializers
from .models import User, Task


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'email', 'mobile_no', 'created_at', 'modified_at']
        
            
class TaskSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)
    assigned_users = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(),many=True, required=False, allow_empty=True)
    
    def create(self, validated_data):        
        assigned_users = validated_data.pop('assigned_users', [])  
        task = Task.objects.create(**validated_data)  
        task.assigned_users.set(assigned_users)  
        return task

    def update(self, instance, validated_data):
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
        