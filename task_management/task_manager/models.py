from django.db import models

from task_manager.base import TimeStampedModel

class User(TimeStampedModel):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    mobile_no = models.CharField(max_length=15, unique=True)
    
    def __str__(self):
        return "User created with id: %s" % (self.id)
    

class Task(TimeStampedModel):
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    TASK_TYPE_CHOICES = [
        ('feature', 'Feature'),
        ('improvement', 'Improvement'),
        ('bug', 'Bug'),
        ('testing', 'Testing'),
        ('deployment', 'Deployment'),
        ('review', 'Code Review'),
        ('support', 'Customer Support'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    task_type = models.CharField(max_length=20, choices=TASK_TYPE_CHOICES, default='feature')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    completed_at = models.CharField(max_length=20, blank=True, null=True)
    assigned_users = models.ManyToManyField(User, related_name="tasks", blank=True, null=True)
    
    def __str__(self):
        return "Task created with id: %s" % (self.id)