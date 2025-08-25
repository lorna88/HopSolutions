from django.db.models import Q
from django.views.generic import DetailView, ListView

from config.settings import TASKS_QUERY_MAP
from .models import Task, Category


class TaskDetailView(DetailView):
    model = Task
    template_name = 'tasks/task-details.html'
    slug_field = 'slug'

class TaskListView(ListView):
    template_name = 'tasks/home.html'
    model = Task
    context_object_name = 'tasks'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

    def get_queryset(self):
        qs = Task.objects.all().select_related('category')

        # filter by category
        categories = self.request.GET.get('categories', None)
        if categories:
            qs = qs.filter(category__slug__in=categories.split(','))

        # search
        to_search = self.request.GET.get('q', None)
        if to_search:
            qs = qs.filter(
                Q(name__icontains=to_search) | Q(comment__icontains=to_search)
            )

        # sort
        qs_key = self.request.GET.get('sort', 'date_asc')
        qs = qs.order_by(TASKS_QUERY_MAP[qs_key])

        return list(qs)