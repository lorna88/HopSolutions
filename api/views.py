import datetime

from django.utils.module_loading import import_string
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiResponse, OpenApiParameter
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import CreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from tags.models import Tag
from .filters import TaskFilter
from .open_api import ErrorSerializer, UNIQUE_SLUG_EXAMPLE, UNIQUE_NAME_EXAMPLE, \
    UNIQUE_SLUG_FOR_NAME_EXAMPLE, UNIQUE_TAGS_EXAMPLE, UNIQUE_SUBTASKS_EXAMPLE, \
    get_not_found_response, get_success_response, OrderValues, get_auth_error_response, WRONG_EMAIL_EXAMPLE, \
    WRONG_USERNAME_EXAMPLE, WRONG_PASSWORD_EXAMPLE, EXISTING_USER_EXAMPLE, LOGIN_USER_REQUEST_EXAMPLE, \
    LOGIN_USER_RESPONSE_EXAMPLE, AUTH_LOGIN_ERROR_EXAMPLE, REFRESH_TOKEN_REQUEST_EXAMPLE, \
    REFRESH_TOKEN_RESPONSE_EXAMPLE, AUTH_REFRESH_ERROR_EXAMPLE
from .permissions import IsOwner
from .serializers import TaskSerializer, CategorySerializer, TagSerializer, UserSerializer
from tasks.models import Task, Category


login_schema_config = extend_schema_view(
    post=extend_schema(
        summary="Login user and retrieve access tokens",
        responses={
            200: get_success_response(import_string(api_settings.TOKEN_OBTAIN_SERIALIZER)),
            401: OpenApiResponse(
                response=ErrorSerializer,
                description='Authentication error',
                examples = [AUTH_LOGIN_ERROR_EXAMPLE]
            ),
        },
        examples=[LOGIN_USER_REQUEST_EXAMPLE, LOGIN_USER_RESPONSE_EXAMPLE]
    )
)

refresh_token_schema_config = extend_schema_view(
    post=extend_schema(
        summary="Retrieve new JWT tokens with refresh token",
        responses={
            200: get_success_response(import_string(api_settings.TOKEN_REFRESH_SERIALIZER)),
            401: OpenApiResponse(
                response=ErrorSerializer,
                description='Authentication error',
                examples = [AUTH_REFRESH_ERROR_EXAMPLE]
            ),
        },
        examples=[REFRESH_TOKEN_REQUEST_EXAMPLE, REFRESH_TOKEN_RESPONSE_EXAMPLE]
    )
)

TokenObtainPairView = login_schema_config(TokenObtainPairView)
TokenRefreshView = refresh_token_schema_config(TokenRefreshView)


class TaskPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'size'
    max_page_size = 20

    def get_paginated_response_schema(self, schema):
        paginated_schema = super().get_paginated_response_schema(schema)
        paginated_schema['properties']['next']['example'] = (
            'http://api.example.org/api/tasks/?{page_query_param}=4'.format(
                page_query_param=self.page_query_param
            )
        )
        paginated_schema['properties']['previous']['example'] = (
            'http://api.example.org/api/tasks/?{page_query_param}=2'.format(
                page_query_param=self.page_query_param
            )
        )
        return paginated_schema


@extend_schema_view(
    list=extend_schema(
        summary="Full list of tasks",
        responses={
            200: get_success_response(TaskSerializer),
            401: get_auth_error_response(),
        },
        parameters=[
            OpenApiParameter("date", type=datetime.date,
                             description='Filter by date'),
            OpenApiParameter("date_after", type=datetime.date,
                             description='Show all tasks with date after specified'),
            OpenApiParameter("date_before", type=datetime.date,
                             description='Show all tasks with date before specified'),
            OpenApiParameter("is_completed", type=bool,
                             description='Show only completed (if true) or active (if false) tasks'),
            OpenApiParameter("category", description='Filter by category name'),
            OpenApiParameter("tag", description='Filter by tag name'),
            OpenApiParameter("ordering", type={'type': 'string'}, enum=OrderValues,
                             description='Which field to use when ordering the results.'),
        ],
    ),
    create=extend_schema(
        summary="Create new task",
        responses={
            201: get_success_response(TaskSerializer),
            400: OpenApiResponse(
                response=ErrorSerializer,
                description='Bad request error',
                examples = [UNIQUE_SLUG_EXAMPLE, UNIQUE_SLUG_FOR_NAME_EXAMPLE, UNIQUE_TAGS_EXAMPLE,
                            UNIQUE_SUBTASKS_EXAMPLE]
            ),
            401: get_auth_error_response(),
        },
    ),
    retrieve=extend_schema(
        summary="View a specific task",
        responses={
            200: get_success_response(TaskSerializer),
            401: get_auth_error_response(),
            404: get_not_found_response('Task'),
        },
    ),
    update=extend_schema(
        summary="Update of specific task",
        responses={
            200: get_success_response(TaskSerializer),
            400: OpenApiResponse(
                response=ErrorSerializer,
                description='Bad request error',
                examples = [UNIQUE_SLUG_EXAMPLE, UNIQUE_TAGS_EXAMPLE, UNIQUE_SUBTASKS_EXAMPLE]
            ),
            401: get_auth_error_response(),
            404: get_not_found_response('Task'),
        },
    ),
    partial_update=extend_schema(
        summary="Partial update of specific task",
        responses={
            200: get_success_response(TaskSerializer),
            400: OpenApiResponse(
                response=ErrorSerializer,
                description='Bad request error',
                examples = [UNIQUE_SLUG_EXAMPLE, UNIQUE_TAGS_EXAMPLE, UNIQUE_SUBTASKS_EXAMPLE]
            ),
            401: get_auth_error_response(),
            404: get_not_found_response('Task'),
        },
    ),
    destroy=extend_schema(
        summary="Delete a specific task",
        responses={
            204: get_success_response(TaskSerializer),
            401: get_auth_error_response(),
            404: get_not_found_response('Task'),
        },
    ),
)
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


@extend_schema_view(
    list=extend_schema(
        summary="Full list of categories",
        responses={
            200: get_success_response(CategorySerializer),
            401: get_auth_error_response(),
        },
    ),
    create=extend_schema(
        summary="Create new category",
        responses={
            201: get_success_response(CategorySerializer),
            400: OpenApiResponse(
                response=ErrorSerializer,
                description='Bad request error',
                examples = [UNIQUE_SLUG_EXAMPLE, UNIQUE_SLUG_FOR_NAME_EXAMPLE]
            ),
            401: get_auth_error_response(),
        },
    ),
    retrieve=extend_schema(
        summary="View a specific category",
        responses={
            200: get_success_response(CategorySerializer),
            401: get_auth_error_response(),
            404: get_not_found_response('Category'),
        },
    ),
    update=extend_schema(
        summary="Update of specific category",
        responses={
            200: get_success_response(CategorySerializer),
            400: OpenApiResponse(
                response=ErrorSerializer,
                description='Bad request error',
                examples = [UNIQUE_SLUG_EXAMPLE]
            ),
            401: get_auth_error_response(),
            404: get_not_found_response('Category'),
        },
    ),
    partial_update=extend_schema(
        summary="Partial update of specific category",
        responses={
            200: get_success_response(CategorySerializer),
            400: OpenApiResponse(
                response=ErrorSerializer,
                description='Bad request error',
                examples = [UNIQUE_SLUG_EXAMPLE]
            ),
            401: get_auth_error_response(),
            404: get_not_found_response('Category'),
        },
    ),
    destroy=extend_schema(
        summary="Delete a specific category",
        responses={
            204: get_success_response(CategorySerializer),
            401: get_auth_error_response(),
            404: get_not_found_response('Category'),
        },
    ),
)
class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, IsOwner]
    filter_backends = []

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Category.objects.none()
        return Category.objects.for_user(self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema_view(
    list=extend_schema(
        summary="Full list of tags",
        responses={
            200: get_success_response(TagSerializer),
            401: get_auth_error_response(),
        },
    ),
    create=extend_schema(
        summary="Create new tag",
        responses={
            201: get_success_response(TagSerializer),
            400: OpenApiResponse(
                response=ErrorSerializer,
                description='Bad request error',
                examples = [UNIQUE_NAME_EXAMPLE]
            ),
            401: get_auth_error_response(),
        },
    ),
    retrieve=extend_schema(
        summary="View a specific tag",
        responses={
            200: get_success_response(TagSerializer),
            401: get_auth_error_response(),
            404: get_not_found_response('Tag'),
        },
    ),
    update=extend_schema(
        summary="Update of specific tag",
        responses={
            200: get_success_response(TagSerializer),
            400: OpenApiResponse(
                response=ErrorSerializer,
                description='Bad request error',
                examples = [UNIQUE_NAME_EXAMPLE]
            ),
            401: get_auth_error_response(),
            404: get_not_found_response('Tag'),
        },
    ),
    partial_update=extend_schema(
        summary="Partial update of specific tag",
        responses={
            200: get_success_response(TagSerializer),
            400: OpenApiResponse(
                response=ErrorSerializer,
                description='Bad request error',
                examples = [UNIQUE_NAME_EXAMPLE]
            ),
            401: get_auth_error_response(),
            404: get_not_found_response('Tag'),
        },
    ),
    destroy=extend_schema(
        summary="Delete a specific tag",
        responses={
            204: get_success_response(TagSerializer),
            401: get_auth_error_response(),
            404: get_not_found_response('Tag'),
        },
    ),
)
class TagViewSet(ModelViewSet):
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    filter_backends = []

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Tag.objects.none()
        return Tag.objects.for_user(self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema_view(
    post=extend_schema(
        summary="Register new user",
        responses={
            201: get_success_response(UserSerializer),
            400: OpenApiResponse(
                response=ErrorSerializer,
                description='Bad request error',
                examples = [WRONG_EMAIL_EXAMPLE, WRONG_USERNAME_EXAMPLE, WRONG_PASSWORD_EXAMPLE,
                            EXISTING_USER_EXAMPLE]
            ),
        },
    ),
)
class RegisterUserView(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = ()
    authentication_classes = ()
