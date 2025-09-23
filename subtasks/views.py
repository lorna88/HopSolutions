from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import View

from subtasks.models import Subtask
from tasks.models import Task


class SubtaskCompleteView(LoginRequiredMixin, View):
    def post(self, request, task_slug, subtask_id, *args, **kwargs):
        subtask = Subtask.objects.get(id=subtask_id)
        is_completed = request.POST.get("is_completed") is not None

        subtask.is_completed = is_completed
        subtask.save()
        return redirect('tasks:task-detail', slug=task_slug)


class SubtaskCreateView(LoginRequiredMixin, View):
    def post(self, request, task_slug, *args, **kwargs):
        name = request.POST.get("name", "New subtask")
        task = Task.objects.get(slug=task_slug)

        subtask = Subtask(name=name, task=task, user=request.user)
        subtask.save()

        return redirect('tasks:task-detail', slug=task_slug)


class SubtaskDeleteView(LoginRequiredMixin, View):
    def post(self, request, task_slug, subtask_id, *args, **kwargs):
        subtask = Subtask.objects.get(id=subtask_id)
        subtask.delete()
        return redirect('tasks:task-detail', slug=task_slug)
