from datetime import datetime

from django.db.models import Q, Prefetch
from django.shortcuts import redirect
from django.views import View
from django.views.generic import ListView, UpdateView, CreateView, DeleteView
from rest_framework.reverse import reverse_lazy

from config.settings import TASKS_QUERY_MAP
from tags.models import Tag
from .forms import TaskUpdateForm, CategoryCreateForm
from .models import Task, Category


class TaskListView(ListView):
    template_name = 'tasks/home.html'
    model = Category
    context_object_name = 'categories'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()

        context['sort_options'] = [
            {'key': 'date_asc', 'label': 'Date ascending'},
            {'key': 'date_desc', 'label': 'Date descending'},
        ]

        context['form'] = CategoryCreateForm()

        return context

    def get_queryset(self):
        qs = Category.objects.all()
        qs_tasks = Task.objects.all()

        # filter by category
        categories = self.request.GET.get('categories', None)
        if categories:
            qs = qs.filter(slug__in=categories.split(','))

        # filter by tag
        tags = self.request.GET.get('tags', None)
        if tags:
            qs_tasks = qs_tasks.filter(tags__name__in=tags.split(','))

        # search
        to_search = self.request.GET.get('q', None)
        if to_search:
            qs = qs.filter(
                Q(tasks__name__icontains=to_search) | Q(tasks__description__icontains=to_search)
            )
            qs_tasks = qs_tasks.filter(
                Q(name__icontains=to_search) | Q(description__icontains=to_search)
            )

        # sort
        qs_key = self.request.GET.get('sort', 'date_asc')
        # qs = qs.order_by(TASKS_QUERY_MAP[qs_key])
        qs_tasks = qs_tasks.order_by(TASKS_QUERY_MAP[qs_key])

        qs = qs.prefetch_related(Prefetch('tasks', queryset=qs_tasks))
        return list(qs)


class TaskDetailView(UpdateView):
    model = Task
    template_name = 'tasks/task-details.html'
    slug_field = 'slug'
    form_class = TaskUpdateForm


class TaskCompleteView(View):
    def post(self, request, slug, *args, **kwargs):
        task = Task.objects.get(slug=slug)
        is_completed = request.POST.get("is_completed") is not None

        task.is_completed = is_completed
        task.save()
        if request.GET.get('next'):
            return redirect(request.GET.get('next'))
        return redirect('tasks:home')


class TaskCreateView(View):
    def post(self, request, *args, **kwargs):
        name = request.POST.get("name", "New task")

        category_slug = request.POST.get("category")
        if category_slug:
            category = Category.objects.get(slug=category_slug)
        else:
            category = Category.objects.first()

        user = request.user

        task = Task(name=name, category=category, user=user)

        date = request.POST.get("date")
        if date:
            date_object = datetime.strptime(date, "%b %d, %Y").date()
            task.date = date_object

        task.save()

        if request.GET.get('next'):
            return redirect(request.GET.get('next'))
        return redirect('tasks:home')


class TaskDeleteView(DeleteView):
    model = Task
    slug_field = 'slug'
    success_url = reverse_lazy("tasks:home")

    def get_success_url(self):
        if self.request.GET.get('next'):
            return self.request.GET.get('next')
        return super().get_success_url()


class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryCreateForm
    success_url = reverse_lazy('tasks:home')
    template_name = 'tasks/add-category.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class CategoryDeleteView(DeleteView):
    model = Category
    slug_field = 'slug'
    success_url = reverse_lazy("tasks:home")


class DeleteCompletedView(View):
    def get(self, request, *args, **kwargs):
        tasks = Task.objects.filter(is_completed=True)
        for task in tasks:
            task.delete()
        return redirect('tasks:home')

