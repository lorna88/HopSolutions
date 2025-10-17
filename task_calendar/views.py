import datetime
from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.views.generic import ListView

from tags.models import Tag
from tasks.models import Task, Category


class MyDayView(LoginRequiredMixin, ListView):
    """Display the list of tasks by the specified date."""
    template_name = 'task_calendar/my_day.html'
    model = Task
    context_object_name = 'tasks'

    def __init__(self, **kwargs):
        """Get the current date."""
        super().__init__(**kwargs)
        today = datetime.date.today()
        self.task_date = today

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """Get the date chosen in the calendar."""
        task_date = request.GET.get('date')
        if task_date:
            date_object = datetime.datetime.strptime(task_date, "%Y-%m-%d")
            self.task_date = date_object
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        """Set parameters into template context"""
        context = super().get_context_data(**kwargs)
        context['date'] = self.task_date
        context['all_categories'] = Category.objects.for_user(self.request.user)
        context['tags'] = Tag.objects.for_user(self.request.user)
        return context

    def get_queryset(self) -> list[Task]:
        """Filter and search options implementation."""
        qs = Task.objects.for_user(self.request.user).filter(date=self.task_date)

        # filter by category
        categories = self.request.GET.get('categories', None)
        if categories:
            qs = qs.filter(category__slug__in=categories.split(','))

        # filter by tag
        tags = self.request.GET.get('tags', None)
        if tags:
            qs = qs.filter(tags__name__in=tags.split(',')).distinct()

        # search
        to_search = self.request.GET.get('q', None)
        if to_search:
            qs = qs.filter(
                Q(name__icontains=to_search) | Q(description__icontains=to_search)
            )

        return list(qs)
