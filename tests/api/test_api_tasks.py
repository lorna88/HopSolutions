import pytest
from django.db.models import Q
from django.urls import reverse

from tasks.models import Task


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

@pytest.mark.django_db
def test_api_tasks_paginate(api_client, authenticated, create_tasks, user_data, tasks_user_data):
    """Testing pagination with a number of elements on a page different from standard."""
    authenticated(user_data)

    query_params = {
        'page': 1,
        'size': 5,
    }
    response = api_client.get(reverse('api:task-list'), query_params)

    assert response.status_code == 200

    data = response.json()
    assert 'count' in data
    assert data['count'] == len(tasks_user_data)
    assert 'next' in data
    assert data['next'] is not None
    assert 'previous' in data
    assert data['previous'] is None

    assert 'results' in data
    results = data['results']
    assert len(results) == query_params['size']

@pytest.mark.django_db
@pytest.mark.parametrize(
    "filter_data",
    [
        {'date': 'tomorrow'},
        {'date_after': 'today'},
        {'category': 'today'},
        {'tag': 'Important'},
    ],
)
def test_api_tasks_filter(api_client, request, authenticated, create_tasks, user_data, filter_data):
    """Checks filtering of tasks data."""
    user = authenticated(user_data)
    db_tasks = Task.objects.for_user(user)

    if 'date' in filter_data:
        filter_data['date'] = request.getfixturevalue(filter_data['date']).strftime('%Y-%m-%d')
        db_tasks = db_tasks.filter(date=filter_data['date'])
    if 'date_after' in filter_data:
        filter_data['date_after'] = request.getfixturevalue(filter_data['date_after']).strftime('%Y-%m-%d')
        db_tasks = db_tasks.filter(date__gte=filter_data['date_after'])
    if 'date_before' in filter_data:
        filter_data['date_before'] = request.getfixturevalue(filter_data['date_before']).strftime('%Y-%m-%d')
        db_tasks = db_tasks.filter(date__lte=filter_data['date_before'])
    if 'is_completed' in filter_data:
        db_tasks = db_tasks.filter(is_completed=filter_data['is_completed'])
    if 'category' in filter_data:
        db_tasks = db_tasks.filter(category__slug=filter_data['category'])
    if 'tag' in filter_data:
        db_tasks = db_tasks.filter(tags__name=filter_data['tag'])

    response = api_client.get(reverse('api:task-list'), filter_data)

    assert response.status_code == 200

    data = response.json()
    assert 'count' in data
    assert data['count'] == db_tasks.count()

    assert 'results' in data
    results = data['results']
    assert len(results) == db_tasks.count()
    for task in results:
        if 'category' in filter_data:
            assert task['category'] == filter_data['category']
        if 'is_completed' in filter_data:
            assert task['is_completed'] == filter_data['is_completed']
        if 'date' in filter_data:
            assert task['date'] == filter_data['date']
        if 'date_after' in filter_data:
            assert task['date'] >= filter_data['date_after']
        if 'date_before' in filter_data:
            assert task['date'] <= filter_data['date_before']
        if 'tag' in filter_data:
            assert any(tag == filter_data['tag'] for tag in task['tags'])

@pytest.mark.django_db
def test_api_tasks_search(api_client, authenticated, create_tasks, user_data):
    """Checks using a search string for tasks data."""
    query_params = {
        'search': 'make'
    }
    user = authenticated(user_data)
    db_tasks = Task.objects.for_user(user).filter(
        Q(name__icontains=query_params['search']) | Q(description__icontains=query_params['search'])
    )

    response = api_client.get(reverse('api:task-list'), query_params)

    assert response.status_code == 200

    data = response.json()
    assert 'count' in data
    assert data['count'] == db_tasks.count()

    assert 'results' in data
    results = data['results']
    assert len(results) == db_tasks.count()
    for task in results:
        assert ((query_params['search'] in task['name'].lower())
                or (query_params['search'] in task['description'].lower()))

@pytest.mark.django_db
@pytest.mark.parametrize(
    "sort",
    ['date', '-date', 'is_completed', '-is_completed', 'category'],
)
def test_api_tasks_order(api_client, request, authenticated, create_tasks, user_data, sort):
    """Checks getting tasks data in a certain order."""
    authenticated(user_data)

    compare = request.getfixturevalue('compare_asc')
    order_field_name = sort
    if sort.startswith('-'):
        compare = request.getfixturevalue('compare_desc')
        order_field_name = sort[1:]

    query_params = {
        'ordering': sort
    }
    response = api_client.get(reverse('api:task-list'), query_params)

    assert response.status_code == 200

    data = response.json()
    assert 'results' in data
    prev_task = None
    for task in data['results']:
        if prev_task:
            assert compare(prev_task, task, order_field_name)
        prev_task = task
