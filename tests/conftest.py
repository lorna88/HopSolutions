import datetime

import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from subtasks.models import Subtask
from tags.models import Tag
from tasks.models import Category, Task
from users.models import User


@pytest.fixture
def user_data():
    """Return data for user login and registration."""
    return {
        'email': 'user@example.com',
        'username': 'user',
        'password': 'strong-password-123',
    }

@pytest.fixture
def other_user_data():
    """Return data for other user login and registration."""
    return {
        'email': 'other_user@example.com',
        'username': 'other_user',
        'password': 'strong-password-456',
    }

@pytest.fixture
def create_user():
    """Fixture for user creation."""
    def create_user_for_data(data):
        return User.objects.create_user(**data)

    return create_user_for_data

@pytest.fixture
def login(client, create_user):
    """Fixture for user login."""
    def login_user_with_data(data):
        user = User.objects.filter(email=data['email']).first()
        if not user:
            user = create_user(data)
        client.login(email=data['email'], password=data['password'])
        return user

    return login_user_with_data

@pytest.fixture
def api_client():
    """Fixture for api client."""
    return APIClient()

@pytest.fixture
def token_pair():
    """Returns dict with access and refresh tokens for user."""
    def get_token_pair(user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    return get_token_pair

@pytest.fixture
def authenticated(api_client, create_user, token_pair):
    """Fixture for API user authentication."""
    def get_client_with_credentials(data):
        user = User.objects.filter(email=data['email']).first()
        if not user:
            user = create_user(data)
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        return user

    return get_client_with_credentials

@pytest.fixture
def today():
    """Fixture for today's date."""
    return datetime.date.today()

@pytest.fixture
def tomorrow():
    """Fixture for tomorrow's date."""
    return datetime.date.today() + datetime.timedelta(days=1)

@pytest.fixture
def in_a_week():
    """Fixture for date in a week."""
    return datetime.date.today() + datetime.timedelta(days=7)

@pytest.fixture
def tasks_user_data(today, tomorrow, in_a_week):
    """Return data for tasks creation by user."""
    return [
        {
            'name': 'Complete project',
            'category': 'today',
            'description': '',
            'date': today,
            'tags': ['Deadline'],
            'subtasks': ['Write tests', 'Create docs']
        },
        {
            'name': 'Go to market',
            'category': 'today',
            'description': '',
            'date': today,
            'tags': ['Important', 'Family'],
            'subtasks': ['Buy fish', 'Buy potatoes']
        },
        {
            'name': 'Read Django guide',
            'category': 'today',
            'description': '',
            'date': today,
            'tags': [],
            'subtasks': []
        },
        {
            'name': 'Write tests and docs',
            'category': 'tomorrow',
            'description': '',
            'date': tomorrow,
            'tags': ['Deadline'],
            'subtasks': []
        },
        {
            'name': 'Make soup',
            'category': 'tomorrow',
            'description': '',
            'date': tomorrow,
            'tags': ['Family'],
            'subtasks': []
        },
        {
            'name': 'Sell old skis',
            'category': 'nearest-time',
            'description': '',
            'date': in_a_week,
            'tags': ['Family'],
            'subtasks': []
        },
    ]

@pytest.fixture
def tasks_other_user_data(today, tomorrow, in_a_week):
    """Return data for tasks creation by other user."""
    return [
        {
            'name': 'Great party',
            'category': 'tomorrow',
            'description': '',
            'date': tomorrow,
            'tags': ['Family'],
            'subtasks': ['Cook the pie', 'Invite relatives and friends']
        },
        {
            'name': 'Feed cat',
            'category': 'today',
            'description': '',
            'date': today,
            'tags': ['Family'],
            'subtasks': []
        },
        {
            'name': 'Go to meeting',
            'category': 'today',
            'description': '',
            'date': today,
            'tags': ['Important'],
            'subtasks': []
        },
        {
            'name': 'Project refactoring',
            'category': 'nearest-time',
            'description': '',
            'date': in_a_week,
            'tags': ['Important'],
            'subtasks': ['First step', 'Second step', 'Third step']
        },
        {
            'name': 'Meet up with friends',
            'category': 'nearest-time',
            'description': '',
            'date': in_a_week,
            'tags': [],
            'subtasks': []
        },
    ]

@pytest.fixture
def create_task():
    """Return function for creating a task."""
    def create_task_for_data(name, category, description, date, tags, subtasks, user):
        task = Task.objects.create(name=name, category=category, description=description, date=date, user=user)
        task.tags.set(tags)
        for subtask in subtasks:
            Subtask.objects.create(name=subtask, task=task, user=user)
        return task

    return create_task_for_data

@pytest.fixture
def create_tasks(create_user, user_data, other_user_data, tasks_user_data, tasks_other_user_data, create_task):
    """Creates tasks for two users with categories and tags."""
    def create_tasks_for_user(user, tasks_data):
        categories = {category.slug: category for category in Category.objects.for_user(user)}
        tags = {tag.name: tag for tag in Tag.objects.for_user(user)}

        for data in tasks_data:
            create_task(
                data['name'],
                categories[data['category']],
                data['description'],
                data['date'],
                [tags[tag_name] for tag_name in data['tags']],
                data['subtasks'],
                user
            )

    create_tasks_for_user(create_user(user_data), tasks_user_data)
    create_tasks_for_user(create_user(other_user_data), tasks_other_user_data)

@pytest.fixture
def task_new_with_category():
    """Return one task data for creation on task list view."""
    return {
        'name': 'New task',
        'category': 'nearest-time',
    }

@pytest.fixture
def task_new_with_date(today):
    """Return one task data for creation on calendar view."""
    return {
        'name': 'New task',
        'date': today,
    }

@pytest.fixture
def task_update(in_a_week):
    """Return one task data for updating."""
    return {
        'name': 'Completed task',
        'category': 'nearest-time',
        'description': 'This task is used for testing any existing task update',
        'date': in_a_week,
        'is_completed': 'on',
    }

@pytest.fixture
def compare_date_asc():
    """Fixture for comparing two tasks by date ascending."""
    def compare_tasks(task1, task2):
        return task1.date <= task2.date

    return compare_tasks

@pytest.fixture
def compare_date_desc():
    """Fixture for comparing two tasks by date descending."""
    def compare_tasks(task1, task2):
        return task1.date >= task2.date

    return compare_tasks
