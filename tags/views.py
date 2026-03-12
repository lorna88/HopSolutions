from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from tasks.services import get_task_by_pk
from .models import Tag
from .services import set_tags_to_task


class TagView(LoginRequiredMixin, View):
    """Modal form for tags choice on task edit page"""
    def get(self, request: HttpRequest, task_id: int, *args, **kwargs) -> HttpResponse:
        """Get all user tags for showing in modal window"""
        tags = Tag.objects.for_user(request.user)
        task = get_task_by_pk(pk=task_id)
        return render(request, 'tags/tag-list.html', {'tags': tags, 'task': task})

    def post(self, request: HttpRequest, task_id: int, *args, **kwargs) -> HttpResponse:
        """Set chosen tags to the task"""
        task = get_task_by_pk(pk=task_id)
        set_tags_to_task(user=request.user, task=task, tag_names=request.POST)

        return redirect('tasks:task-detail', username=request.user.username, slug=task.slug)
