from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from tasks.models import Task
from .models import Tag


class TagView(LoginRequiredMixin, View):
    """Modal form for tags choice on task edit page"""
    def get(self, request: HttpRequest, task_id: int, *args, **kwargs) -> HttpResponse:
        """Get all user tags for showing in modal window"""
        tags = Tag.objects.for_user(request.user)
        task = get_object_or_404(Task, id=task_id)
        return render(request, 'tags/tag-list.html', {'tags': tags, 'task': task})

    def post(self, request: HttpRequest, task_id: int, *args, **kwargs) -> HttpResponse:
        """Set chosen tags to the task"""
        task = get_object_or_404(Task, id=task_id)
        task.tags.clear()

        tags = Tag.objects.for_user(request.user).filter(name__in=request.POST)
        task.tags.add(*tags)
        task.save()

        return redirect('tasks:task-detail', username=request.user.username, slug=task.slug)
