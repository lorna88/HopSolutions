from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView

from tasks.models import Task
from .models import Tag


class TagView(View):
    def get(self, request, task_id, *args, **kwargs):
        tags = Tag.objects.all()
        task = Task.objects.get(id=task_id)
        return render(request, 'tags/tag-list.html', {'tags': tags, 'task': task})

    def post(self, request, task_id, *args, **kwargs):
        task = Task.objects.get(id=task_id)
        task.tags.clear()

        tags = Tag.objects.filter(name__in=request.POST)
        task.tags.add(*tags)
        task.save()

        return redirect('tasks:task-detail', slug=task.slug)
