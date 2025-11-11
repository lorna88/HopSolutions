import pytest
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse

from tasks.models import Task


@pytest.mark.django_db
def test_api_task_create(api_client, authenticated, create_tasks, user_data, task_new_with_many_fields):
    """Testing successful task creation."""
    user = authenticated(user_data)
    task_data = task_new_with_many_fields.copy()
    task_data['subtasks'] =[{'name': subtask} for subtask in task_data['subtasks']]

    response = api_client.post(reverse('api:task-list'), task_data, format='json')

    assert response.status_code == 201

    data = response.json()
    assert isinstance(data, dict)
    assert data.get('name') == task_data['name']

    task = Task.objects.for_user(user).get(name=task_data['name'])
    assert task.name == task_data['name']
    assert task.category.slug == task_data['category']
    assert task.date == task_data['date']
    assert {tag.name for tag in task.tags.all()} == set(task_data['tags'])
    assert {subtask.name for subtask in task.subtasks.all()} == set(task_new_with_many_fields['subtasks'])

@pytest.mark.django_db
def test_api_existing_task_create(api_client, authenticated, create_tasks, user_data, tasks_user_data):
    """Creation of existing task must fail."""
    authenticated(user_data)
    task_user = tasks_user_data[0]
    task_data = {
        'name': task_user['name'],
        'category': task_user['category']
    }

    response = api_client.post(reverse('api:task-list'), task_data, format='json')

    assert response.status_code == 400

    data = response.json()
    assert data['name'] == ["A slug for this name already exists."]

@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_fixture, task_fixture",
    [
        ('user_data', 'tasks_user_data'),
        ('other_user_data', 'tasks_other_user_data'),
    ],
)
def test_api_task_detail_success(api_client, request, authenticated, create_tasks, user_fixture, task_fixture):
    """Testing user's task viewing."""
    user = authenticated(request.getfixturevalue(user_fixture))
    task_data = request.getfixturevalue(task_fixture)[0]
    task = Task.objects.for_user(user).get(name=task_data['name'])

    response = api_client.get(reverse('api:task-detail', args=[task.id]))

    assert response.status_code == 200

    task = response.json()
    assert isinstance(task, dict)
    assert task['name'] == task_data['name']
    assert task['category'] == task_data['category']
    assert task['description'] == task_data['description']
    assert task['date'] == task_data['date'].strftime('%Y-%m-%d')
    assert set(task['tags']) == set(task_data['tags'])
    assert {subtask['name'] for subtask in task['subtasks']} == set(task_data['subtasks'])
    assert task['user'] == user.username

@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_fixture, task_fixture",
    [
        ('user_data', 'tasks_other_user_data'),
        ('other_user_data', 'tasks_user_data'),
    ],
)
def test_api_task_detail_fail(api_client, request, authenticated, create_tasks, user_fixture, task_fixture):
    """Testing someone else's task viewing."""
    authenticated(request.getfixturevalue(user_fixture))
    task_data = request.getfixturevalue(task_fixture)[0]
    task = Task.objects.get(name=task_data['name'])

    response = api_client.get(reverse('api:task-detail', args=[task.id]))

    assert response.status_code == 404

@pytest.mark.django_db
def test_api_task_update(api_client, authenticated, create_tasks, user_data, tasks_user_data, task_update_tags_subtasks):
    """Testing successful task updating."""
    user = authenticated(user_data)
    task = Task.objects.for_user(user).get(name=tasks_user_data[0]['name'])
    task_data = task_update_tags_subtasks.copy()

    response = api_client.put(reverse('api:task-detail', args=[task.id]), task_data, format='json')

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, dict)
    assert data['name'] == task_data['name']

    task.refresh_from_db()
    assert task.name == task_data['name']
    assert task.category.slug == task_data['category']
    assert task.description == task_data['description']
    assert task.date == task_data['date']
    assert task.is_completed == (task_data.get('is_completed') == 'on')
    assert {tag.name for tag in task.tags.all()} == set(task_data['tags'])
    assert task.subtasks.count() == len(task_data['subtasks'])
    for subtask_data in task_data['subtasks']:
        subtask = task.subtasks.get(name=subtask_data['name'])
        if 'is_completed' in subtask_data:
            assert subtask.is_completed == (subtask_data['is_completed'] == 'on')


@pytest.mark.django_db
def test_api_task_delete(api_client, authenticated, create_tasks, user_data, tasks_user_data):
    """Testing successful task deleting."""
    user = authenticated(user_data)
    task_id = Task.objects.for_user(user).get(name=tasks_user_data[0]['name']).id

    response = api_client.delete(reverse('api:task-detail', args=[task_id]))

    assert response.status_code == 204

    with pytest.raises(ObjectDoesNotExist):
        Task.objects.get(id=task_id)
