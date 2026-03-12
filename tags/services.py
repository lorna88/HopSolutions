from django.contrib.auth.models import AnonymousUser
from django.db import transaction

from tags.models import Tag
from tasks.models import Task
from users.models import User


@transaction.atomic
def set_tags_to_task(*,
                     user: User | AnonymousUser,
                     task: Task,
                     tag_names: dict) -> None:
    """
    Sets specified tag names to the task
    """
    task.tags.clear()
    tags = Tag.objects.for_user(user).filter(name__in=tag_names)
    task.tags.add(*tags)
    task.save()  # type: ignore[no-untyped-call]