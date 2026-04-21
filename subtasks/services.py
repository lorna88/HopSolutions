from django.shortcuts import get_object_or_404

from subtasks.models import Subtask
from tasks.models import Task
from tasks.services import NonUniqueObjectError


class NonUniqueSubtaskNameError(NonUniqueObjectError):
    """
    An exception thrown when attempting to create
    a subtask with name that already exists
    """
    def __init__(self, task: Task, name: str):
        self.task = task
        self.name = name
        self.message = 'Name must be unique for each subtask!'
        super().__init__(self.message)


def subtask_complete(*, subtask_id: int, is_completed: bool) -> None:
    """
    Gets the subtask by pk and changes the value of its field "is_completed"
    """
    subtask = get_object_or_404(Subtask, id=subtask_id)
    subtask.is_completed = is_completed
    subtask.save()  # type: ignore[no-untyped-call]


def subtask_create(*, name: str, task: Task) -> Subtask:
    """
    Creates the subtask with specified name for the task.
    Raises an exception if the name is not unique.
    """
    if not name:
        raise ValueError('The new subtask is missing a name.')

    # Name validation - name must be unique for the task
    if Subtask.objects.filter(task=task, name=name).exists():
        raise NonUniqueSubtaskNameError(task, name)

    subtask = Subtask.objects.create(name=name, task=task)
    return subtask


def subtask_delete(*, pk: int) -> None:
    """
    Deletes a subtask specified by ID
    """
    subtask = get_object_or_404(Subtask, id=pk)
    subtask.delete()
