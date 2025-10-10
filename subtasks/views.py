from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.views import View

from subtasks.models import Subtask
from tasks.models import Task


class SubtaskCompleteView(LoginRequiredMixin, View):
    """Make a subtask completed or active"""
    def post(
            self,
            request: HttpRequest,
            task_slug: str,
            subtask_id: int,
            *args, **kwargs) -> HttpResponse:
        """Update subtask status on form post"""
        subtask = get_object_or_404(Subtask, id=subtask_id)
        is_completed = request.POST.get("is_completed") is not None

        subtask.is_completed = is_completed
        subtask.save()
        return redirect('tasks:task-detail', slug=task_slug)


class SubtaskCreateView(LoginRequiredMixin, View):
    """Create a new subtask"""
    def post(self, request: HttpRequest, task_slug: str, *args, **kwargs) -> HttpResponse:
        """Create a new task on form post"""
        name = request.POST.get("name")
        task = get_object_or_404(Task, slug=task_slug)
        Subtask.objects.create(name=name, task=task)

        return redirect('tasks:task-detail', slug=task_slug)


class SubtaskDeleteView(LoginRequiredMixin, View):
    """Delete the subtask"""
    def post(
            self,
            request: HttpRequest,
            task_slug: str,
            subtask_id: int,
            *args, **kwargs) -> HttpResponse:
        """Delete the subtask on form post"""
        subtask = get_object_or_404(Subtask, id=subtask_id)
        subtask.delete()
        return redirect('tasks:task-detail', slug=task_slug)
