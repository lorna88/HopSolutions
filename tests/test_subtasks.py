import pytest
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse

from subtasks.models import Subtask
from tasks.models import Task


@pytest.mark.django_db
def test_subtask_creation(client, create_tasks, login, user_data, tasks_user_data):
    """
    Testing successful subtask creation.
    """
    user = login(user_data)
    task_data = tasks_user_data[0]
    task = Task.objects.for_user(user).get(name=task_data['name'])

    reverse_to_task_detail = reverse('tasks:task-detail', kwargs={
        'username': user.username,
        'slug': task.slug
    })
    subtask_data = {'name': 'Running linters and formatters'}

    url = reverse('subtasks:create', kwargs={'task_slug': task.slug})
    response = client.post(url, subtask_data, follow=True)

    assert response.status_code == 200
    assert response.request['PATH_INFO'] == reverse_to_task_detail

    task.refresh_from_db()
    assert task.subtasks.count() == len(task_data['subtasks']) + 1
    assert subtask_data['name'] in [subtask.name for subtask in task.subtasks.all()]

@pytest.mark.django_db
def test_subtask_complete(client, create_tasks, login, user_data, tasks_user_data):
    """
    Testing subtask completing.
    """
    user = login(user_data)
    task_data = tasks_user_data[0]
    task = Task.objects.for_user(user).get(name=task_data['name'])
    subtask = task.subtasks.get(name=task_data['subtasks'][0])

    reverse_to_task_detail = reverse('tasks:task-detail', kwargs={
        'username': user.username,
        'slug': task.slug
    })
    subtask_data = {'is_completed': 'on'}

    url = reverse('subtasks:complete', kwargs={'task_slug': task.slug, 'subtask_id': subtask.id})
    response = client.post(url, subtask_data, follow=True)

    assert response.status_code == 200
    assert response.request['PATH_INFO'] == reverse_to_task_detail

    task.refresh_from_db()
    assert task.subtasks.count() == len(task_data['subtasks'])
    subtask.refresh_from_db()
    assert subtask.name == task_data['subtasks'][0]
    assert subtask.is_completed == True

@pytest.mark.django_db
def test_subtask_delete(client, create_tasks, login, user_data, tasks_user_data):
    """
    Testing subtask completing.
    """
    user = login(user_data)
    task_data = tasks_user_data[0]
    task = Task.objects.for_user(user).get(name=task_data['name'])
    subtask = task.subtasks.get(name=task_data['subtasks'][0])

    reverse_to_task_detail = reverse('tasks:task-detail', kwargs={
        'username': user.username,
        'slug': task.slug
    })

    url = reverse('subtasks:delete', kwargs={'task_slug': task.slug, 'subtask_id': subtask.id})
    response = client.post(url, follow=True)

    assert response.status_code == 200
    assert response.request['PATH_INFO'] == reverse_to_task_detail

    task.refresh_from_db()
    assert task.subtasks.count() == len(task_data['subtasks']) - 1

    with pytest.raises(ObjectDoesNotExist):
        task.subtasks.get(name=task_data['subtasks'][0])
