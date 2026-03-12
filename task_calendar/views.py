from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.views.generic import ListView

from tags.models import Tag
from task_calendar.services import DateProvider
from tasks.models import Task, Category
from tasks.selectors import get_tasks


class MyDayView(LoginRequiredMixin, ListView):
    """Display the list of tasks by the specified date."""
    template_name = 'task_calendar/my_day.html'
    model = Task
    context_object_name = 'tasks'

    def __init__(self, **kwargs):
        """Initialization of the date provider."""
        super().__init__(**kwargs)
        self.date_provider = None

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """Get the date chosen in the calendar."""
        self.date_provider = DateProvider(date=request.GET.get('date'))
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        """Set parameters into template context"""
        context = super().get_context_data(**kwargs)
        context['date'] = self.date_provider.get_date()
        context['all_categories'] = Category.objects.for_user(self.request.user)
        context['tags'] = Tag.objects.for_user(self.request.user)
        return context

    def get_queryset(self) -> list[Task]:  # type: ignore[override]
        """Filter and search options implementation."""
        qs = get_tasks(
            user=self.request.user,
            date=self.date_provider.get_date(),
            categories=self.request.GET.get('categories', None),
            tags=self.request.GET.get('tags', None),
            to_search=self.request.GET.get('q', None)
        )
        return list(qs)
