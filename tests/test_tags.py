from urllib.parse import urlencode

import pytest
from django.urls import reverse

from tags.models import Tag
from tasks.models import Task


@pytest.mark.django_db
def test_get_tag_list(client, create_tasks, login, user_data, task_user):
    """Testing tag list view for a task."""
    user = login(user_data)
    task = Task.objects.for_user(user).get(name=task_user['name'])

    url = reverse(
        'tags:tag-list',
        kwargs={'task_id': task.id}
    )
    response = client.get(url)

    assert response.status_code == 200

    task = response.context['task']
    assert task.name == task_user['name']
    assert task.category.slug == task_user['category']
    assert task.user == user
    assert {tag.name for tag in task.tags.all()} == set(task_user['tags'])

    tags = response.context['tags']
    assert set(tags) == set(Tag.objects.for_user(user))

@pytest.mark.django_db
def test_set_tag_list(client, create_tasks, login, user_data, task_user):
    """
    Testing tags replacement to the task.
    """
    user = login(user_data)
    task = Task.objects.for_user(user).get(name=task_user['name'])

    reverse_to_task_detail = reverse('tasks:task-detail', kwargs={
        'username': user.username,
        'slug': task.slug
    })
    query_params = {'next': reverse_to_task_detail}
    url = f'{reverse('tags:tag-list', kwargs={'task_id': task.id})}?{urlencode(query_params)}'

    tags_data = {
        'Important': '',
        'Deadline': '',
        'Family': ''
    }
    response = client.post(url, tags_data, follow=True)

    assert response.status_code == 200
    assert response.request['PATH_INFO'] == reverse_to_task_detail

    task.refresh_from_db()
    assert {tag.name for tag in task.tags.all()} == tags_data.keys()
