from django.db import models
from drf_spectacular.utils import OpenApiResponse, OpenApiExample
from rest_framework import serializers

# =============================================================================
# Examples for object uniqueness errors
# =============================================================================

UNIQUE_SLUG_EXAMPLE = OpenApiExample(
    'Unique slug',
    summary='unique slug error',
    description='An error occurs when trying to assign an existing slug to an object.',
    value={
        'slug': 'A slug must be unique.',
    },
    response_only=True,
)

UNIQUE_SLUG_FOR_NAME_EXAMPLE = OpenApiExample(
    'Unique slug for name',
    summary='unique slug for name error',
    description='An error occurs when trying to create a new object with name that is \
    used for making slug. And this slug duplicates the existing one.',
    value={
        'name': 'A slug for this name already exists.',
    },
    response_only=True,
)

UNIQUE_NAME_EXAMPLE = OpenApiExample(
    'Unique name',
    summary='unique name error',
    description='An error occurs when trying to assign an existing name to an object.',
    value={
        'name': 'A name must be unique.',
    },
    response_only=True,
)

UNIQUE_TAGS_EXAMPLE = OpenApiExample(
    'Unique tags',
    summary='unique tags error',
    description='An error occurs when trying to add repetitive tag names to an object.',
    value={
        'tags': 'The list of tags must not contain duplicates.',
    },
    response_only=True,
)

UNIQUE_SUBTASKS_EXAMPLE = OpenApiExample(
    'Unique subtasks',
    summary='unique subtasks error',
    description='An error occurs when trying to add repetitive subtask names to an object.',
    value={
        'subtasks': 'The list of subtasks must not contain duplicates.',
    },
    response_only=True,
)

# =============================================================================
# Examples for user registration and authentication
# =============================================================================

WRONG_EMAIL_EXAMPLE = OpenApiExample(
    'Wrong email',
    summary='incorrect email error',
    description='An error occurs when trying to register user with incorrect email address.',
    value={
        'email': ['Enter a valid email address.'],
    },
    response_only=True,
)

WRONG_USERNAME_EXAMPLE = OpenApiExample(
    'Wrong username',
    summary='incorrect username error',
    description='An error occurs if username contains any incorrect symbols.',
    value={
        'username': ['Enter a valid username. This value may contain only latin letters, numbers, and -/_ characters.'],
    },
    response_only=True,
)

WRONG_PASSWORD_EXAMPLE = OpenApiExample(
    'Wrong password',
    summary='incorrect password error',
    description='An error occurs if the password does not meet accepted standards.',
    value={
        'password': [
            "This password is too short. It must contain at least 8 characters.",
            "This password is too common."
        ],
    },
    response_only=True,
)

EXISTING_USER_EXAMPLE = OpenApiExample(
    'User already exists',
    summary='existing user error',
    description='An error occurs when trying to register user with an existing email address and username.',
    value={
        'email': ["User with this email already exists."],
        'username': ["A user with that username already exists."],
    },
    response_only=True,
)

LOGIN_USER_REQUEST_EXAMPLE = OpenApiExample(
    'Login request',
    summary='login request example',
    description='example for user login with correct credentials',
    value={
        'email': 'user@example.com',
        'password': 'strong-password-123',
    },
    request_only=True,
)

LOGIN_USER_RESPONSE_EXAMPLE = OpenApiExample(
    'Login response',
    summary='login response example',
    description='example for response on user login with correct credentials',
    value={
        'refresh': 'secret.refresh.token',
        'access': 'secret.access.token',
    },
    response_only=True,
)

AUTH_LOGIN_ERROR_EXAMPLE = OpenApiExample(
    'Login error',
    summary='authentication error',
    description='An error occurs when trying to login with incorrect email or password.',
    value={
        'detail': 'No active account found with the given credentials',
    },
    response_only=True,
)

REFRESH_TOKEN_REQUEST_EXAMPLE = OpenApiExample(
    'Token refresh request',
    summary='token refresh request example',
    description='example for updating token pair with refresh token',
    value={
        'refresh': 'secret.refresh.token',
    },
    request_only=True,
)

REFRESH_TOKEN_RESPONSE_EXAMPLE = OpenApiExample(
    'Token refresh response',
    summary='token refresh response example',
    description='example for response of refreshing token pair',
    value={
        'refresh': 'secret.refresh.token',
        'access': 'secret.access.token',
    },
    response_only=True,
)

AUTH_REFRESH_ERROR_EXAMPLE = OpenApiExample(
    'Token refresh error',
    summary='authentication error',
    description='An error occurs when trying to get new token pair with incorrect refresh token.',
    value={
        'detail': 'Token is invalid',
        'code': 'token_not_valid',
    },
    response_only=True,
)


class OrderValues(models.TextChoices):
    DATE_ASC = 'date', 'date ascending'
    DATE_DESC = '-date', 'date descending'
    IS_COMPLETED_ASC = 'is_completed', 'is_completed ascending'
    IS_COMPLETED_DESC = '-is_completed', 'is_completed descending'
    CATEGORY_SLUG_ASC = 'category__slug', 'category slug ascending'
    CATEGORY_SLUG_DESC = '-category__slug', 'category slug descending'


class ErrorSerializer(serializers.Serializer):
    detail = serializers.CharField(max_length=200)


def get_auth_error_response():
    return OpenApiResponse(
        response=ErrorSerializer,
        description='Authentication error',
        examples=[
            OpenApiExample(
                'Response',
                summary='authentication error',
                description='An error occurs if a request is made without providing an access JWT token in the request header.',
                value={
                    'detail': 'Authentication credentials were not provided.',
                },
                response_only=True,
            ),
        ]
    )

def get_not_found_response(model_name):
    return OpenApiResponse(
        response=ErrorSerializer,
        description='Not found error',
        examples = [
            OpenApiExample(
                'Response',
                summary='not found error',
                description='An error occurs when accessing an object by a non-existent ID.',
                value={
                    'detail': f'No {model_name} matches the given query.',
                },
                response_only=True,
            ),
        ]
    )

def get_success_response(serializer_class):
    return OpenApiResponse(
        response=serializer_class,
        description='Successful response',
    )