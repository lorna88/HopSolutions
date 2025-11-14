from django.db import models
from drf_spectacular.utils import OpenApiResponse, OpenApiExample
from rest_framework import serializers


class OrderValues(models.TextChoices):
    DATE_ASC = 'date', 'date ascending'
    DATE_DESC = '-date', 'date descending'
    IS_COMPLETED_ASC = 'is_completed', 'is_completed ascending'
    IS_COMPLETED_DESC = '-is_completed', 'is_completed descending'
    CATEGORY_SLUG_ASC = 'category__slug', 'category slug ascending'
    CATEGORY_SLUG_DESC = '-category__slug', 'category slug descending'


class ErrorSerializer(serializers.Serializer):
    detail = serializers.CharField(max_length=200)


AUTHENTICATION_ERROR_RESPONSE = OpenApiResponse(
    response=ErrorSerializer,
    description='Authentication error',
    examples = [
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