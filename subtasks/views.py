from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.views import View

from subtasks.models import Subtask
from tasks.models import Task


class SubtaskCompleteView(LoginRequiredMixin, View):
    def post(self, request, task_slug, subtask_id, *args, **kwargs):
        subtask = get_object_or_404(Subtask, id=subtask_id)
        is_completed = request.POST.get("is_completed") is not None

        subtask.is_completed = is_completed
        subtask.save()
        return redirect('tasks:task-detail', slug=task_slug)


class SubtaskCreateView(LoginRequiredMixin, View):
    def post(self, request, task_slug, *args, **kwargs):
        name = request.POST.get("name")
        task = get_object_or_404(Task, slug=task_slug)
        Subtask.objects.create(name=name, task=task)

        return redirect('tasks:task-detail', slug=task_slug)


class SubtaskDeleteView(LoginRequiredMixin, View):
    def post(self, request, task_slug, subtask_id, *args, **kwargs):
        subtask = get_object_or_404(Subtask, id=subtask_id)
        subtask.delete()
        return redirect('tasks:task-detail', slug=task_slug)
