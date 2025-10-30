import pytest
from django.urls import reverse
from pytest_django.fixtures import client

from tags.models import Tag
from tasks.models import Category


@pytest.mark.django_db
@pytest.mark.parametrize(
    "login_fixture, tasks_data_fixture",
    [
        ('login_user', 'tasks_user_data'),
        ('login_other_user', 'tasks_other_user_data'),
    ],
)
def test_tasks_list_view(client, request, create_tasks, login_fixture, tasks_data_fixture):
    """Checks that every user gets only his own tasks."""
    user = request.getfixturevalue(login_fixture)
    tasks_data = request.getfixturevalue(tasks_data_fixture)
    db_categories = Category.objects.for_user(user)
    db_tags = Tag.objects.for_user(user)

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
            if task.tags.exists():
                assert task.tags.all().first() in list(db_tags)
