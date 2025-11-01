from urllib.parse import urlencode

import pytest
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.utils.text import slugify

from tasks.models import Category, Task


@pytest.mark.django_db
def test_task_creation(client, create_tasks, login, user_data, task_new, today):
    """
    Testing successful task creation.
    """
    user = login(user_data)
    task_data = task_new.copy()
    task_data['category'] = Category.objects.for_user(user).get(slug=task_data['category']).pk

    query_params = {'next': reverse('tasks:home')}
    url = f'{reverse('tasks:task-create')}?{urlencode(query_params)}'

    response = client.post(url, task_data, follow=True)

    assert response.status_code == 200
    assert response.request['PATH_INFO'] == reverse('tasks:home')

    new_task = Task.objects.for_user(user).get(name=task_data['name'])
    assert new_task.category.slug == 'nearest-time'
    assert new_task.date == today

@pytest.mark.django_db
def test_existing_task_creation(client, create_tasks, login, user_data, task_user):
    """
    Creation of existing task must fail.
    """
    user = login(user_data)
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
def test_task_detail_success(client, request, create_tasks, login, user_fixture, task_fixture):
    """Testing user's task viewing."""
    user = login(request.getfixturevalue(user_fixture))
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
    assert task.date == task_data['date']
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
def test_task_detail_fail(client, request, create_tasks, login, user_fixture, task_fixture):
    """Testing someone else's task viewing."""
    login(request.getfixturevalue(user_fixture))
    task = Task.objects.get(name=request.getfixturevalue(task_fixture)['name'])

    url = reverse(
        'tasks:task-detail',
        kwargs={'username': task.user.username, 'slug': task.slug}
    )
    response = client.get(url)

    assert response.status_code == 404

@pytest.mark.django_db
def test_task_update(client, create_tasks, login, user_data, task_user, task_update, in_a_week):
    """
    Testing successful task updating.
    """
    user = login(user_data)
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
    assert task.date == in_a_week
    assert task.is_completed == (task_update.get('is_completed') == 'on')

@pytest.mark.django_db
def test_task_delete(client, create_tasks, login, user_data, task_user):
    """
    Testing successful task deleting.
    """
    user = login(user_data)
    task_pk = Task.objects.for_user(user).get(name=task_user['name']).pk

    query_params = {'next': reverse('tasks:home')}
    url = f'{reverse('tasks:task-delete',
                     kwargs={'pk': task_pk}
                     )}?{urlencode(query_params)}'

    response = client.post(url, follow=True)

    assert response.status_code == 200
    assert response.request['PATH_INFO'] == reverse('tasks:home')

    with pytest.raises(ObjectDoesNotExist):
        Task.objects.get(pk=task_pk)
