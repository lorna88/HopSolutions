import pytest

from users.models import User


@pytest.fixture
def correct_user_data():
    """Return correct data for user login and registration."""
    return {
        'email': 'testuser@example.com',
        'username': 'testuser',
        'password': 'strong-password-123',
    }

@pytest.fixture
def incorrect_user_data():
    """Return wrong data for user login and registration."""
    return {
        'email': 'baduser@example.com',
        'username': 'baduser',
        'password': 'strong-password-456',
    }

@pytest.fixture
def create_user(correct_user_data):
    """Fixture for user creation."""
    User.objects.create_user(**correct_user_data)

@pytest.fixture
def login_user(client, create_user, correct_user_data):
    """Fixture for user creation and login."""
    client.login(email=correct_user_data['email'], password=correct_user_data['password'])
