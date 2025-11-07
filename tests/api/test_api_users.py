import pytest
from django.urls import reverse

from users.models import User


@pytest.mark.django_db
def test_api_user_registration_success(api_client, user_data):
    """
    Testing successful user registration.
    """
    response = api_client.post(reverse('api:register'), user_data)

    assert response.status_code == 201

    data = response.json()
    assert data['email'] == user_data['email']
    assert data['username'] == user_data['username']
    assert 'password' not in data

    assert User.objects.filter(username=user_data['username']).exists()

@pytest.mark.django_db
@pytest.mark.parametrize(
    "wrong_data, errors",
    [
        ({'email': 'user.example.com'}, {'email': ['Enter a valid email address.']}),
        ({'username': 'user.'}, {'username': ['Enter a valid username. This value may contain only latin letters, numbers, and -/_ characters.']}),
        ({'password': 'password'}, {'password': ['This password is too common.']}),
    ],
)
def test_api_user_registration_wrong(api_client, user_data, wrong_data, errors):
    """
    Testing user registration with wrong data.
    """
    data = user_data.copy()
    for key in wrong_data:
        data[key] = wrong_data[key]

    response = api_client.post(reverse('api:register'), data)

    assert response.status_code == 400

    response_data = response.json()
    for error in errors:
        assert response_data[error] == errors[error]

@pytest.mark.django_db
def test_api_existing_user_registration(api_client, create_user, user_data):
    """
    Registration of existing user must fail.
    """
    create_user(user_data)
    response = api_client.post(reverse('api:register'), user_data)

    assert response.status_code == 400

    data = response.json()
    assert data['email'] == ["User with this email already exists."]
    assert data['username'] == ["A user with that username already exists."]

@pytest.mark.django_db
def test_api_user_login_success(api_client, create_user, user_data):
    """
    Testing successful login. Receiving access/refresh tokens pair.
    """
    create_user(user_data)
    response = api_client.post(reverse('api:login'), user_data)

    assert response.status_code == 200

    data = response.json()
    assert 'access' in data
    assert 'refresh' in data

@pytest.mark.django_db
def test_api_user_login_wrong(api_client, create_user, user_data, other_user_data):
    """
    Testing login with wrong credentials.
    """
    create_user(user_data)
    response = api_client.post(reverse('api:login'), other_user_data)

    assert response.status_code == 401

    data = response.json()
    assert 'detail' in data
    assert data['detail'] == "No active account found with the given credentials"

@pytest.mark.django_db
def test_api_user_refresh_success(api_client, create_user, user_data, token_pair):
    """
    Checks receiving new access token with existing refresh token.
    """
    user = create_user(user_data)
    token = token_pair(user)
    response = api_client.post(reverse('api:login_refresh'), {'refresh': token['refresh']})

    assert response.status_code == 200

    data = response.json()
    assert 'access' in data
    assert data['access'] != token['access']
