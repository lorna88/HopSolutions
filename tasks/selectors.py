from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.db.models import Count, Q, Prefetch, QuerySet

from tasks.models import Category, Task
from users.models import User

def get_tasks(*,
              user: User | AnonymousUser,
              date: datetime.date = None,
              categories: str = None,
              tags: str = None,
              to_search: str = None,
              sort_key: str = None) -> QuerySet:  # type: ignore[override]
    """
    Get queryset of tasks for the user with filtering by tags,
    searching by search string and sorting by specified key.
    """
    qs = Task.objects.for_user(user)

    # filter by date
    if date:
        qs = qs.filter(date=date)

    # filter by category
    if categories:
        qs = qs.filter(category__slug__in=categories.split(','))

    # filter by tag
    if tags:
        qs = qs.filter(tags__name__in=tags.split(',')).distinct()

    # search
    if to_search:
        qs = qs.filter(
            Q(name__icontains=to_search) | Q(description__icontains=to_search)
        )

    # sort
    if sort_key:
        qs = qs.order_by(settings.TASKS_QUERY_MAP[sort_key])

    return qs

def get_categories(*,
                   user: User | AnonymousUser,
                   categories: str = None,
                   tags: str = None,
                   to_search: str = None,
                   sort_key: str = None) -> QuerySet:  # type: ignore[override]
    """
    Get queryset of categories for the user with filtering by tags,
    searching by search string and sorting by specified key.
    May be limited by the specified slugs of categories.
    """
    qs = Category.objects.for_user(user)

    # filter by category
    if categories:
        qs = qs.filter(slug__in=categories.split(','))

    # filter by tag
    if tags:
        qs = qs.annotate(
            tasks_count=Count(
                'tasks',
                filter=Q(tasks__tags__name__in=tags.split(','))
            )
        ).filter(tasks_count__gt=0)

    # search
    if to_search:
        qs = qs.filter(
            Q(tasks__name__icontains=to_search) | Q(tasks__description__icontains=to_search)
        ).distinct()

    qs_tasks = get_tasks(user=user, tags=tags, to_search=to_search, sort_key=sort_key)
    qs = qs.prefetch_related(Prefetch('tasks', queryset=qs_tasks))
    return qs