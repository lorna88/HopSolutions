import datetime

from django.views.generic import ListView

from tasks.models import Task


class MyDayView(ListView):
    template_name = 'task_calendar/my_day.html'
    model = Task
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        today = datetime.date.today()
        context['date'] = today

        return context

    def get_queryset(self):
        today = datetime.date.today()
        qs = Task.objects.filter(date=today)
        return list(qs)