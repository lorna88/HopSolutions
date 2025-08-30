from django.db.models import Q
from django.template.context_processors import request
from django.views import View
from django.views.generic import DetailView, ListView, UpdateView, CreateView
from rest_framework.reverse import reverse_lazy

from config.settings import TASKS_QUERY_MAP
from .forms import TaskUpdateForm, TaskCreateForm
from .models import Task, Category


class TaskListView(ListView):
    template_name = 'tasks/home.html'
    model = Category
    context_object_name = 'categories'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['categories'] = Category.objects.all()

        context['sort_options'] = [
            {'key': 'date_asc', 'label': 'Date ascending'},
            {'key': 'date_desc', 'label': 'Date descending'},
        ]

        # categories = context['categories']
        # for category in categories:
        #     category.form = TaskCreateForm(category)
        # context['categories'] = categories
        context['form'] = TaskCreateForm()
        return context

    def get_queryset(self):
        qs = Category.objects.all().prefetch_related('tasks')

        # filter by category
        categories = self.request.GET.get('categories', None)
        if categories:
            qs = qs.filter(slug__in=categories.split(','))

        # search
        to_search = self.request.GET.get('q', None)
        if to_search:
            qs = qs.filter(
                Q(tasks__name__icontains=to_search) | Q(tasks__description__icontains=to_search)
            )

        # sort
        # qs_key = self.request.GET.get('sort', 'date_asc')
        # qs = qs.order_by(TASKS_QUERY_MAP[qs_key])

        return list(qs)


class TaskDetailView(UpdateView):
    model = Task
    template_name = 'tasks/task-details.html'
    slug_field = 'slug'
    form_class = TaskUpdateForm


class TaskCreateView(CreateView):
    model = Task
    template_name = 'tasks/home.html'
    form_class = TaskCreateForm
    success_url = reverse_lazy('tasks:home')

class TaskView(View):
    def get(self, request, *args, **kwargs):
        view = TaskListView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = TaskCreateView.as_view()
        return view(request, *args, **kwargs)