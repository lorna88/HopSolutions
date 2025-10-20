from rest_framework.viewsets import ModelViewSet

from tags.models import Tag
from .serializers import TaskSerializer, CategorySerializer, TagSerializer
from tasks.models import Task, Category


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
