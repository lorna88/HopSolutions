from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import CreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from tags.models import Tag
from .filters import TaskFilter
from .permissions import IsOwner
from .serializers import TaskSerializer, CategorySerializer, TagSerializer, UserSerializer
from tasks.models import Task, Category


class TaskPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'size'
    max_page_size = 20


class TaskViewSet(ModelViewSet):
    serializer_class = TaskSerializer
    pagination_class = TaskPagination
    permission_classes = [IsAuthenticated, IsOwner]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = TaskFilter
    search_fields = ['name', 'description']
    ordering_fields = ['category__slug', 'date', 'is_completed']
    ordering = ['category__slug']

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Task.objects.none()
        return Task.objects.for_user(self.request.user).select_related('category').prefetch_related('tags', 'subtasks')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @extend_schema(
        responses={
            200: inline_serializer(
                name='CustomPaginatedResponse',
                fields={
                    'count': serializers.IntegerField(help_text='Общее количество элементов'),
                    'next': serializers.URLField(
                        allow_null=True,
                        help_text='URL следующей страницы',
                        example='https://api.example.com/api/tasks/?page=4'
                    ),
                    'previous': serializers.URLField(
                        allow_null=True,
                        help_text='URL предыдущей страницы',
                        example='https://api.example.com/api/tasks/?page=2'
                    ),
                    'results': TaskSerializer(many=True, help_text='Список задач'),
                }
            )
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Category.objects.none()
        return Category.objects.for_user(self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TagViewSet(ModelViewSet):
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Tag.objects.none()
        return Tag.objects.for_user(self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RegisterUserView(CreateAPIView):
    serializer_class = UserSerializer
