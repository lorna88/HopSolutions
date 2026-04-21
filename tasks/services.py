from datetime import datetime

from django.contrib.auth.models import AnonymousUser
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils.text import slugify

from subtasks.models import Subtask
from tasks.models import Task, Category
from users.models import User


class TaskManagerError(Exception):
    """ A base class for all project exceptions"""
    pass


class NonUniqueObjectError(TaskManagerError):
    """
    A base class for exceptions thrown when attempting to create
    an object that already exists
    """
    pass


class NonUniqueTaskSlugError(NonUniqueObjectError):
    """
    An exception thrown when attempting to create
    a task with slug that already exists
    """
    def __init__(self, slug: str):
        self.slug = slug
        self.message = f'A task with slug "{slug}" is already exists.'
        super().__init__(self.message)


def task_complete(*, pk: int, is_completed: bool) -> None:
    """
    Gets the task by pk and changes the value of its field "is_completed"
    """
    task = get_task_by_pk(pk=pk)
    task.is_completed = is_completed
    task.save()  # type: ignore[no-untyped-call]


def task_new_validate(**fields) -> None:
    """
    Validates task fields such as name, slug and category
    """
    user = fields.get('user')

    name = fields.get('name')
    if not name:
        raise ValueError('The new task is missing a name.')

    slug = fields.get('slug')
    if Task.objects.for_user(user).filter(slug=slug).exists():
        raise NonUniqueTaskSlugError(slug)

    category = fields.get('category')
    if not category:
        raise ValueError('No category specified for the new task.')


@transaction.atomic
def task_create(validate=False, **fields) -> Task:
    """
    Creates the task with specified name. The slug is computing automatically.
    A category either is specified or the first one for this user is taken.
    If specified the date is marked.
    """
    user = fields.get('user')
    name = fields.get('name')

    slug = fields.get('slug')
    if not slug:
        slug = slugify(name)
        fields['slug'] = slug

    category = fields.get('category')
    if category:
        if isinstance(category, int) or isinstance(category, str):
            category = Category.objects.get(pk=category)
    elif Category.objects.for_user(user).exists():
        category = (
            Category.objects.for_user(user).first()  # type: ignore[assignment]
        )
    else:
        category = None
    fields['category'] = category

    date = fields.get('date')
    if date:
        if isinstance(date, str):
            date = datetime.strptime(date, "%b %d, %Y").date()
            fields['date'] = date

    if validate:
        task_new_validate(**fields)

    subtasks_data = fields.pop('subtasks', [])
    tags_data = fields.pop('tags', [])

    task = Task.objects.create(**fields)  # type: ignore[misc]

    for subtask_data in subtasks_data:
        Subtask.objects.create(task=task, user=user, **subtask_data)
    if tags_data:
        task.tags.set(tags_data)

    return task


@transaction.atomic
def task_update(task: Task, **fields) -> Task:
    """
    Updates fields in task including tags and subtasks
    """
    tags_data = fields.pop('tags', None)
    subtasks_data = fields.pop('subtasks', None)

    for attr, value in fields.items():
        setattr(task, attr, value)
    task.save()  # type: ignore[no-untyped-call]

    if tags_data is not None:
        task.tags.set(tags_data)

    if subtasks_data is not None:
        task_subtasks = {sub.name: sub for sub in task.subtasks.all()}

        # noinspection PyTypeChecker
        for subtask in subtasks_data:
            subtask_name = subtask["name"]
            if subtask_name not in task_subtasks.keys():
                task.subtasks.create(task=task, user=task.user, **subtask)
            else:
                task_subtasks.pop(subtask_name)
                Subtask.objects.filter(name=subtask_name).update(**subtask)

        for subtask in task_subtasks.values():
            subtask.delete()

    return task


def task_delete_completed(*, user: User | AnonymousUser) -> int:
    """
    Deletes all completed tasks. Returns the number of tasks deleted.
    """
    tasks = Task.objects.for_user(user).filter(is_completed=True)
    _, deleted_objects = tasks.delete()
    deleted_count = deleted_objects.get('tasks.Task', 0)
    return deleted_count


def get_task_by_pk(*, pk: int) -> Task:
    """
    Returns the task by its ID or gives an exception
    """
    return get_object_or_404(Task, pk=pk)


def get_task_by_user_and_slug(*, user: User | AnonymousUser, slug: str) -> Task:
    """
    Returns the task by its user and slug or gives an exception
    """
    return get_object_or_404(Task.objects.for_user(user), slug=slug)
