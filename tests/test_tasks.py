import datetime
from urllib.parse import urlencode

import pytest
from django.urls import reverse
from django.utils.text import slugify
from pytest_django.fixtures import client

from tasks.models import Category, Task


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_fixture, tasks_data_fixture",
    [
        ('user_data', 'tasks_user_data'),
        ('other_user_data', 'tasks_other_user_data'),
    ],
)
def test_tasks_list_view(client, request, create_tasks, login_user, user_fixture, tasks_data_fixture):
    """Checks that every user gets only his own tasks."""
    user = login_user(request.getfixturevalue(user_fixture))
    tasks_data = {data['name']: data for data in request.getfixturevalue(tasks_data_fixture)}
    db_categories = Category.objects.for_user(user)

    url = reverse('tasks:home')
    response = client.get(url)

    assert response.status_code == 200
    categories = response.context['categories']
    assert len(categories) == 3
    assert set(categories) == set(db_categories)

    for category in categories:
        tasks = category.tasks.all()

        for task in tasks:
            assert task.name in tasks_data
            tags = tasks_data[task.name]['tags']
            assert task.tags.count() == len(tags)
            if task.tags.exists():
                assert task.tags.all().first().name in tags

@pytest.mark.django_db
def test_task_creation(client, create_tasks, login_user, user_data, task_new):
    """
    Testing successful task creation.
    """
    user = login_user(user_data)
    task_data = task_new.copy()
    task_data['category'] = Category.objects.for_user(user).get(slug=task_data['category']).pk

    query_params = {'next': reverse('tasks:home')}
    url = f'{reverse('tasks:task-create')}?{urlencode(query_params)}'

    response = client.post(url, task_data, follow=True)

    assert response.status_code == 200
    assert response.request['PATH_INFO'] == reverse('tasks:home')

    new_task = Task.objects.for_user(user).get(name=task_data['name'])
    assert new_task.category.slug == 'nearest-time'
    assert new_task.date == datetime.datetime.strptime('2025-10-31', "%Y-%m-%d").date()

@pytest.mark.django_db
def test_existing_task_creation(client, create_tasks, login_user, user_data, task_user):
    """
    Creation of existing task must fail.
    """
    user = login_user(user_data)
    task_data = task_user.copy()
    task_data['category'] = Category.objects.for_user(user).get(slug=task_data['category']).pk
    initial_tasks_count = Task.objects.count()

    query_params = {'next': reverse('tasks:home')}
    url = f'{reverse('tasks:task-create')}?{urlencode(query_params)}'

    response = client.post(url, task_data, follow=True)

    assert response.status_code == 200
    assert response.request['PATH_INFO'] == reverse('tasks:home')
    final_tasks_count = Task.objects.count()
    assert initial_tasks_count == final_tasks_count

@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_fixture, task_fixture",
    [
        ('user_data', 'task_user'),
        ('other_user_data', 'task_other_user'),
    ],
)
def test_task_detail_success(client, request, create_tasks, login_user, user_fixture, task_fixture):
    """Testing user's task viewing."""
    user = login_user(request.getfixturevalue(user_fixture))
    task_data = request.getfixturevalue(task_fixture)

    url = reverse(
        'tasks:task-detail',
        kwargs={'username': user.username, 'slug': slugify(task_data['name'])}
    )
    response = client.get(url)

    assert response.status_code == 200
    task = response.context['task']
    assert task.name == task_data['name']
    assert task.category.slug == task_data['category']
    assert task.user == user
    # assert {tag.name for tag in task.tags.all()} == set(task_data['tags'])

@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_fixture, task_fixture",
    [
        ('user_data', 'task_other_user'),
        ('other_user_data', 'task_user'),
    ],
)
def test_task_detail_fail(client, request, create_tasks, login_user, user_fixture, task_fixture):
    """Testing someone else's task viewing."""
    login_user(request.getfixturevalue(user_fixture))
    task = Task.objects.get(name=request.getfixturevalue(task_fixture)['name'])

    url = reverse(
        'tasks:task-detail',
        kwargs={'username': task.user.username, 'slug': task.slug}
    )
    response = client.get(url)

    assert response.status_code == 404

@pytest.mark.django_db
def test_task_update(client, create_tasks, login_user, user_data, task_user, task_update):
    """
    Testing successful task creation.
    """
    user = login_user(user_data)
    task = Task.objects.for_user(user).get(name=task_user['name'])
    task_data = task_update.copy()
    task_data['category'] = Category.objects.for_user(user).get(slug=task_data['category']).pk

    query_params = {'next': reverse('tasks:home')}
    url = f'{reverse('tasks:task-detail',
                     kwargs={'username': user.username, 'slug': task.slug}
                     )}?{urlencode(query_params)}'

    response = client.post(url, task_data, follow=True)

    assert response.status_code == 200
    assert response.request['PATH_INFO'] == reverse('tasks:home')

    task.refresh_from_db()
    assert task.name == task_update['name']
    assert task.category.slug == task_update['category']
    assert task.description == task_update['description']
    assert task.date == datetime.datetime.strptime(task_update['date'], "%Y-%m-%d").date()
    assert task.is_completed == (task_update.get('is_completed') is not None)
