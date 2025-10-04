from datetime import datetime

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q, Prefetch
from django.shortcuts import redirect
from django.views import View
from django.views.generic import ListView, UpdateView, CreateView, DeleteView
from rest_framework.reverse import reverse_lazy

from config.settings import TASKS_QUERY_MAP
from tags.models import Tag
from .forms import TaskUpdateForm, CategoryCreateForm
from .models import Task, Category


class TaskListView(LoginRequiredMixin, ListView):
    template_name = 'tasks/home.html'
    model = Category
    context_object_name = 'categories'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_categories'] = Category.objects.filter(user=self.request.user)
        context['tags'] = Tag.objects.filter(user=self.request.user)

        context['sort_options'] = [
            {'key': 'date_asc', 'label': 'Date ascending'},
            {'key': 'date_desc', 'label': 'Date descending'},
        ]

        context['form'] = CategoryCreateForm()

        return context

    def get_queryset(self):
        qs = Category.objects.filter(user=self.request.user)
        qs_tasks = Task.objects.filter(user=self.request.user)

        # filter by category
        categories = self.request.GET.get('categories', None)
        if categories:
            qs = qs.filter(slug__in=categories.split(','))

        # filter by tag
        tags = self.request.GET.get('tags', None)
        if tags:
            qs_tasks = qs_tasks.filter(tags__name__in=tags.split(',')).distinct()

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


class TaskDetailView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    template_name = 'tasks/task-details.html'
    slug_field = 'slug'
    form_class = TaskUpdateForm
    success_message = "Task was updated successfully: %(name)s"

    def get_context_data(self, **kwargs):
        kwargs['form'] = TaskUpdateForm(instance=self.object, user=self.request.user)
        context = super().get_context_data(**kwargs)

        if self.request.GET.get('next'):
            context['next'] = self.request.GET.get('next')
        return context


class TaskCompleteView(LoginRequiredMixin, View):
    def post(self, request, slug, *args, **kwargs):
        task = Task.objects.get(slug=slug)
        is_completed = request.POST.get("is_completed") is not None

        task.is_completed = is_completed
        task.save()
        if request.GET.get('next'):
            return redirect(request.GET.get('next'))
        return redirect('tasks:home')


class TaskCreateView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        name = request.POST.get("name")
        category_slug = request.POST.get("category")
        if category_slug:
            category = Category.objects.get(slug=category_slug)
        else:
            category = Category.objects.first()

        date_object = None
        date = request.POST.get("date")
        if date:
            date_object = datetime.strptime(date, "%b %d, %Y").date()

        task = Task.objects.create(name=name, category=category, date=date_object, user=request.user)
        messages.success(request, f'Task created successfully: {task.name}')

        if request.GET.get('next'):
            return redirect(request.GET.get('next'))
        return redirect('tasks:home')

class TaskDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Task
    slug_field = 'slug'
    success_url = reverse_lazy("tasks:home")

    def get_success_url(self):
        if self.request.GET.get('next'):
            return self.request.GET.get('next')
        return super().get_success_url()

    def get_success_message(self, cleaned_data):
        return f"Task was deleted: {self.object.name}"


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryCreateForm
    success_url = reverse_lazy('tasks:home')
    template_name = 'tasks/add-category.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, f'Category created successfully: {form.instance.name}')
        return super().form_valid(form)


class CategoryDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Category
    slug_field = 'slug'
    success_url = reverse_lazy("tasks:home")

    def get_success_message(self, cleaned_data):
        return f"Category was deleted: {self.object.name}"


class DeleteCompletedView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        tasks = Task.objects.filter(is_completed=True, user=self.request.user)
        for task in tasks:
            task.delete()
        messages.success(self.request, 'All completed tasks were deleted')
        return redirect('tasks:home')

