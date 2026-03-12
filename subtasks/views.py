from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.views import View

from subtasks.services import subtask_complete, subtask_create, NonUniqueSubtaskNameError, subtask_delete
from tasks.services import get_task_by_user_and_slug


class SubtaskCompleteView(LoginRequiredMixin, View):
    """Make a subtask completed or active"""
    def post(
            self,
            request: HttpRequest,
            task_slug: str,
            subtask_id: int,
            *args, **kwargs) -> HttpResponse:
        """Update subtask status on form post"""
        subtask_complete(
            subtask_id=subtask_id,
            is_completed=request.POST.get("is_completed") is not None
        )

        return redirect('tasks:task-detail', username=request.user.username, slug=task_slug)


class SubtaskCreateView(LoginRequiredMixin, View):
    """Create a new subtask"""
    def post(self, request: HttpRequest, task_slug: str, *args, **kwargs) -> HttpResponse:
        """Create a new task on form post"""
        try:
            subtask_create(
                name=request.POST.get("name"),
                task=get_task_by_user_and_slug(user=request.user, slug=task_slug)
            )
        except NonUniqueSubtaskNameError as e:
            messages.error(request, e.message)

        return redirect('tasks:task-detail', username=request.user.username, slug=task_slug)


class SubtaskDeleteView(LoginRequiredMixin, View):
    """Delete the subtask"""
    def post(
            self,
            request: HttpRequest,
            task_slug: str,
            subtask_id: int,
            *args, **kwargs) -> HttpResponse:
        """Delete the subtask on form post"""
        subtask_delete(pk=subtask_id)
        return redirect('tasks:task-detail', username=request.user.username, slug=task_slug)
