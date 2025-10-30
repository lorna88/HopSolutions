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
def create_user(user_data):
    """Fixture for user creation."""
    return User.objects.create_user(**user_data)

@pytest.fixture
def create_other_user(other_user_data):
    """Fixture for other user creation."""
    return User.objects.create_user(**other_user_data)

@pytest.fixture
def login_user(client, create_user, user_data):
    """Fixture for user creation and login."""
    client.login(email=user_data['email'], password=user_data['password'])
    return create_user

@pytest.fixture
def login_other_user(client, create_other_user, other_user_data):
    """Fixture for other user creation and login."""
    client.login(email=other_user_data['email'], password=other_user_data['password'])
    return create_other_user

@pytest.fixture
def tasks_user_data():
    """Return data for task creation by user."""
    return ['Complete project', 'Go to market', 'Read Django guide', 'Write tests and docs', 'Make soup', 'Sell old skis']

@pytest.fixture
def tasks_other_user_data():
    """Return data for task creation by other user."""
    return ['Feed cat', 'Go to meeting', 'Project refactoring', 'Meet up with friends', 'Great party']

@pytest.fixture
def create_tasks(create_user, create_other_user, tasks_user_data, tasks_other_user_data):
    """Creates tasks for two users with categories and tags."""
    user = create_user
    categories_user = {category.name: category for category in Category.objects.for_user(user)}
    tags_user = {tag.name: tag for tag in Tag.objects.for_user(user)}
    tasks_user = {name: Task(name=name, user=user) for name in tasks_user_data}

    tasks_user['Complete project'].category = categories_user['Today']
    tasks_user['Go to market'].category = categories_user['Today']
    tasks_user['Read Django guide'].category = categories_user['Today']
    tasks_user['Write tests and docs'].category = categories_user['Tomorrow']
    tasks_user['Make soup'].category = categories_user['Tomorrow']
    tasks_user['Sell old skis'].category = categories_user['Nearest time']

    for task_name in tasks_user:
        tasks_user[task_name].save()

    tasks_user['Complete project'].tags.add(tags_user['Deadline'])
    tasks_user['Go to market'].tags.add(tags_user['Important'], tags_user['Family'])
    tasks_user['Write tests and docs'].tags.add(tags_user['Deadline'])
    tasks_user['Make soup'].tags.add(tags_user['Family'])
    tasks_user['Sell old skis'].tags.add(tags_user['Family'])

    other_user = create_other_user
    categories_other_user = {category.name: category for category in Category.objects.for_user(other_user)}
    tags_other_user = {tag.name: tag for tag in Tag.objects.for_user(other_user)}

    tasks_other_user = {name: Task(name=name, user=other_user) for name in tasks_other_user_data}

    tasks_other_user['Feed cat'].category = categories_other_user['Today']
    tasks_other_user['Go to meeting'].category = categories_other_user['Today']
    tasks_other_user['Project refactoring'].category = categories_other_user['Nearest time']
    tasks_other_user['Meet up with friends'].category = categories_other_user['Nearest time']
    tasks_other_user['Great party'].category = categories_other_user['Tomorrow']

    for task in tasks_other_user.values():
        task.save()

    tasks_other_user['Go to meeting'].tags.add(tags_other_user['Important'])
    tasks_other_user['Project refactoring'].tags.add(tags_other_user['Important'])
    tasks_other_user['Feed cat'].tags.add(tags_other_user['Family'])
    tasks_other_user['Great party'].tags.add(tags_other_user['Family'])

