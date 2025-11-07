import pytest
from django.urls import reverse


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_fixture, tasks_data_fixture",
    [
        ('user_data', 'tasks_user_data'),
        ('other_user_data', 'tasks_other_user_data'),
    ],
)
def test_api_tasks_list(api_client, request, authenticated, create_tasks, user_fixture, tasks_data_fixture):
    """Checks that every user gets only his own tasks."""
    user = authenticated(request.getfixturevalue(user_fixture))
    tasks_data = {data['name']: data for data in request.getfixturevalue(tasks_data_fixture)}

    response = api_client.get(reverse('api:task-list'))

    assert response.status_code == 200

    data = response.json()
    assert 'count' in data
    assert data['count'] == len(tasks_data)
    assert 'next' in data
    assert data['next'] is None
    assert 'previous' in data
    assert data['previous'] is None

    assert 'results' in data
    results = data['results']
    assert len(results) == len(tasks_data)
    for task in results:
        task_data = tasks_data[task['name']]
        assert task['name'] == task_data['name']
        assert task['category'] == task_data['category']
        assert task['description'] == task_data['description']
        assert task['date'] == task_data['date'].strftime('%Y-%m-%d')
        assert set(task['tags']) == set(task_data['tags'])
        assert {subtask['name'] for subtask in task['subtasks']} == set(task_data['subtasks'])
        assert task['user'] == user.username




