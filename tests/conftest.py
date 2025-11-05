import datetime

import pytest

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
def create_task():
    """Return function for creating a task."""
    def create_task_for_data(name, category, date, tags, user):
        task = Task.objects.create(name=name, category=category, date=date, user=user)
        task.tags.set(tags)
        return task

    return create_task_for_data

@pytest.fixture
def tasks_user_data(today, tomorrow, in_a_week):
    """Return data for tasks creation by user."""
    return [
        {'name': 'Complete project', 'category': 'today', 'date': today, 'tags': ['Deadline']},
        {'name': 'Go to market', 'category': 'today', 'date': today, 'tags': ['Important', 'Family']},
        {'name': 'Read Django guide', 'category': 'today', 'date': today, 'tags': []},
        {'name': 'Write tests and docs', 'category': 'tomorrow', 'date': tomorrow, 'tags': ['Deadline']},
        {'name': 'Make soup', 'category': 'tomorrow', 'date': tomorrow, 'tags': ['Family']},
        {'name': 'Sell old skis', 'category': 'nearest-time', 'date': in_a_week, 'tags': ['Family']},
    ]

@pytest.fixture
def tasks_other_user_data(today, tomorrow, in_a_week):
    """Return data for tasks creation by other user."""
    return [
        {'name': 'Feed cat', 'category': 'today', 'date': today, 'tags': ['Family']},
        {'name': 'Go to meeting', 'category': 'today', 'date': today, 'tags': ['Important']},
        {'name': 'Project refactoring', 'category': 'nearest-time', 'date': in_a_week, 'tags': ['Important']},
        {'name': 'Meet up with friends', 'category': 'nearest-time', 'date': in_a_week, 'tags': []},
        {'name': 'Great party', 'category': 'tomorrow', 'date': tomorrow, 'tags': ['Family']},
    ]

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
                data['date'],
                [tags[tag_name] for tag_name in data['tags']],
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
def task_user(today):
    """Return data of existing user's task."""
    return {
        'name': 'Complete project',
        'category': 'today',
        'description': '',
        'date': today,
        'tags': ['Deadline'],
    }

@pytest.fixture
def task_other_user(tomorrow):
    """Return data of existing other user's task."""
    return {
        'name': 'Great party',
        'category': 'tomorrow',
        'description': '',
        'date': tomorrow,
        'tags': ['Family']
    }
