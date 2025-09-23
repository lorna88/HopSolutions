from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View

from tasks.models import Task
from .models import Tag


class TagView(LoginRequiredMixin, View):
    def get(self, request, task_id, *args, **kwargs):
        tags = Tag.objects.filter(user=request.user)
        task = Task.objects.get(id=task_id)
        return render(request, 'tags/tag-list.html', {'tags': tags, 'task': task})

    def post(self, request, task_id, *args, **kwargs):
        task = Task.objects.get(id=task_id)
        task.tags.clear()

        tags = Tag.objects.filter(name__in=request.POST, user=request.user)
        task.tags.add(*tags)
        task.save()

        return redirect('tasks:task-detail', slug=task.slug)
