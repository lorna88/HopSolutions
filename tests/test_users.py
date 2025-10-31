import pytest
from django.urls import reverse

from users.models import User


@pytest.mark.django_db
def test_user_registration_success(client, user_data):
    """
    Testing successful user registration.
    """
    registration_url = reverse('users:register')
    response = client.post(registration_url, {
        'email': user_data['email'],
        'username': user_data['username'],
        'password1': user_data['password'],
        'password2': user_data['password']
    }, follow=True)

    assert response.status_code == 200
    assert response.request['PATH_INFO'] == reverse('users:login')
    assert User.objects.filter(username=user_data['username']).exists()

@pytest.mark.django_db
def test_existing_user_registration(client, create_user, user_data):
    """
    Registration of existing user must fail.
    """
    create_user(user_data)
    registration_url = reverse('users:register')
    initial_users_count = User.objects.count()
    response = client.post(registration_url, {
        'email': user_data['email'],
        'username': user_data['username'],
        'password1': user_data['password'],
        'password2': user_data['password']
    })

    assert response.status_code == 200
    assert response.request['PATH_INFO'] == reverse('users:register')
    final_users_count = User.objects.count()
    assert initial_users_count == final_users_count

@pytest.mark.django_db
def test_wrong_password_user_registration(client, user_data, other_user_data):
    """
    User registration with different passwords must fail.
    """
    registration_url = reverse('users:register')
    initial_users_count = User.objects.count()
    response = client.post(registration_url, {
        'email': user_data['email'],
        'username': user_data['username'],
        'password1': user_data['password'],
        'password2': other_user_data['password']
    })

    assert response.status_code == 200
    assert response.request['PATH_INFO'] == reverse('users:register')
    final_users_count = User.objects.count()
    assert initial_users_count == final_users_count


@pytest.mark.django_db
def test_login_success(client, create_user, user_data):
    """Testing successful login."""
    create_user(user_data)
    login_url = reverse('users:login')
    response = client.post(login_url, {
        'username': user_data['email'],
        'password': user_data['password']
    }, follow=True)

    assert response.status_code == 200
    assert response.request['PATH_INFO'] == reverse('tasks:home')
    assert response.wsgi_request.user.is_authenticated

@pytest.mark.django_db
def test_wrong_credentials_login(client, create_user, user_data, other_user_data):
    """Testing login with incorrect email and password."""
    create_user(user_data)
    login_url = reverse('users:login')
    response = client.post(login_url, {
        'username': other_user_data['email'],
        'password': other_user_data['password']
    })

    assert response.status_code == 200
    assert response.request['PATH_INFO'] == reverse('users:login')
    assert not response.wsgi_request.user.is_authenticated
