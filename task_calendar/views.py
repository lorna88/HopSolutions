import datetime

from django.views.generic import ListView

from tasks.models import Task


class MyDayView(ListView):
    template_name = 'task_calendar/my_day.html'
    model = Task
    context_object_name = 'tasks'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        today = datetime.date.today()
        self.task_date = today

    def get(self, request, *args, **kwargs):
        task_date = request.GET.get('date')
        if task_date:
            date_object = datetime.datetime.strptime(task_date, "%Y-%m-%d")
            self.task_date = date_object
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['date'] = self.task_date
        return context

    def get_queryset(self):
        qs = Task.objects.filter(date=self.task_date)
        return list(qs)