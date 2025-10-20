from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import TaskViewSet, CategoryViewSet, TagViewSet

app_name = 'api'

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'tags', TagViewSet, basename='tag')

urlpatterns = [
    path('', include(router.urls)),
]