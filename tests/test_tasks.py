from urllib.parse import urlencode

import pytest
from django.db.models import Q
from django.urls import reverse
from pytest_django.fixtures import client

from tasks.models import Category, Task
from tests.conftest import today


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_fixture, tasks_data_fixture",
    [
        ('user_data', 'tasks_user_data'),
        ('other_user_data', 'tasks_other_user_data'),
    ],
)
def test_tasks_list_view(client, request, create_tasks, login, user_fixture, tasks_data_fixture):
    """Checks that every user gets only his own tasks."""
    user = login(request.getfixturevalue(user_fixture))
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
@pytest.mark.parametrize(
    "user_fixture, tasks_data_fixture, date_fixture",
    [
        ('user_data', 'tasks_user_data', 'today'),
        ('user_data', 'tasks_user_data', 'tomorrow'),
        ('other_user_data', 'tasks_other_user_data', 'today'),
        ('other_user_data', 'tasks_other_user_data', 'in_a_week'),
    ],
)
def test_calendar_view(client, request, create_tasks, login, user_fixture, tasks_data_fixture, date_fixture, today):
    """Gets task list for different users and dates on calendar view."""
    login(request.getfixturevalue(user_fixture))

    date = request.getfixturevalue(date_fixture)
    tasks_data = {data['name']: data for data in request.getfixturevalue(tasks_data_fixture) if data['date'] == date}

    query_params = {}
    if date_fixture != today:
        query_params = {
            'date': date,
        }
    url = reverse('calendar:my_day')
    response = client.get(url, query_params)

    assert response.status_code == 200
    tasks = response.context['tasks']
    assert len(tasks) == len(tasks_data)

    for task in tasks:
        assert task.name in tasks_data
        tags = tasks_data[task.name]['tags']
        assert task.tags.count() == len(tags)
        if task.tags.exists():
            assert task.tags.all().first().name in tags

@pytest.mark.django_db
@pytest.mark.parametrize(
    "filter_data",
    [
        {'categories': 'today'},
        {'tags': 'Important'},
        {'q': 'Task'},
        {
            'categories': 'today',
            'tags': 'Deadline',
        },
        {
            'categories': 'today,tomorrow',
            'tags': 'Deadline',
        },
        {
            'categories': 'tomorrow',
            'tags': 'Deadline,Family',
        },
        {
            'categories': 'today',
            'tags': 'Deadline',
            'q': 'Task',
        },
    ],
)
def test_tasks_list_filter_search(client, create_tasks, login, user_data, filter_data):
    """Checks that every user gets only his own tasks."""
    user = login(user_data)
    filter_categories = filter_data.get('categories')
    # if filter_categories:
    #     filter_categories = filter_categories.split(',')
    filter_tags = filter_data.get('tags')
    # if filter_tags:
    #     filter_tags = filter_tags.split(',')
    search_string = filter_data.get('q')
    # if search_string:
    #     search_string = search_string.lower()

    db_tasks = Task.objects.for_user(user)
    if filter_categories:
        filter_categories = filter_categories.split(',')
        db_tasks = db_tasks.filter(category__slug__in=filter_categories).distinct()
    if filter_tags:
        filter_tags = filter_tags.split(',')
        db_tasks = db_tasks.filter(tags__name__in=filter_tags).distinct()
    if search_string:
        search_string = search_string.lower()
        db_tasks = db_tasks.filter(Q(name__icontains=search_string) | Q(description__icontains=search_string))

    category_slugs = list({task.category.slug for task in db_tasks})

    url = reverse('tasks:home')
    response = client.get(url, filter_data)

    assert response.status_code == 200
    total_tasks_count = 0

    categories = response.context['categories']
    assert len(categories) == len(category_slugs)
    for category in categories:
        if filter_categories:
            assert category.slug in filter_categories
        tasks_count = category.tasks.count()
        assert tasks_count > 0
        total_tasks_count += tasks_count

        tasks = category.tasks.all()
        for task in tasks:
            if search_string:
                assert (search_string in task.name.lower()) or (search_string in task.description.lower())
            if filter_tags:
                assert any(tag.name in filter_tags for tag in task.tags.all())

    assert total_tasks_count == db_tasks.count()