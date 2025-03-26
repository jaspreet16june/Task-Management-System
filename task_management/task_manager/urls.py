from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, UserViewSet

# Create a DefaultRouter instance to handle automatic URL routing for ViewSets
router = DefaultRouter()

# Register UserViewSet with the router under the 'users' endpoint and TaskViewset with the router under the 'tasks'
router.register(r'tasks', TaskViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
