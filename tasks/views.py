from django.views.generic import DetailView, ListView

from .models import Task, Category


class TaskDetailView(DetailView):
    model = Task
    template_name = 'tasks/task-details.html'
    slug_field = 'slug'

class TaskListView(ListView):
    template_name = 'tasks/home.html'
    model = Task
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context
