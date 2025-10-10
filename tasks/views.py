from datetime import datetime
from typing import Any

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q, Prefetch
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, UpdateView, CreateView, DeleteView

from config.settings import TASKS_QUERY_MAP
from tags.models import Tag
from .forms import TaskUpdateForm, CategoryCreateForm
from .models import Task, Category


class TaskListView(LoginRequiredMixin, ListView):
    """Display the list of categories with its tasks."""
    template_name = 'tasks/home.html'
    model = Category
    context_object_name = 'categories'
    paginate_by = 3

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        """Set parameters into template context"""
        context = super().get_context_data(**kwargs)
        context['all_categories'] = Category.objects.filter(user=self.request.user)
        context['tags'] = Tag.objects.filter(user=self.request.user)

        context['sort_options'] = [
            {'key': 'date_asc', 'label': 'Date ascending'},
            {'key': 'date_desc', 'label': 'Date descending'},
        ]

        context['form'] = CategoryCreateForm()

        return context

    def get_queryset(self) -> list[Category]:
        """Filter, search and sort options implementation."""
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
    """Display the specified task info and handle its updating"""
    model = Task
    template_name = 'tasks/task-details.html'
    slug_field = 'slug'
    form_class = TaskUpdateForm
    success_message = "Task was updated successfully: %(name)s"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        """Set parameters into template context"""
        kwargs['form'] = TaskUpdateForm(instance=self.object, user=self.request.user)
        context = super().get_context_data(**kwargs)

        if self.request.GET.get('next'):
            context['next'] = self.request.GET.get('next')
        return context


class TaskCompleteView(LoginRequiredMixin, View):
    """Make a task completed or active"""
    def post(self, request: HttpRequest, slug: str, *args, **kwargs) -> HttpResponse:
        """Update task status on form post"""
        task = get_object_or_404(Task, slug=slug)
        is_completed = request.POST.get("is_completed") is not None

        task.is_completed = is_completed
        task.save()
        if request.GET.get('next'):
            return redirect(request.GET.get('next'))
        return redirect('tasks:home')


class TaskCreateView(LoginRequiredMixin, View):
    """Create a new task"""
    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """Create a new task on form post"""
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

        task = Task.objects.create(
            name=name,
            category=category,
            date=date_object,
            user=request.user)
        messages.success(request, f'Task created successfully: {task.name}')

        if request.GET.get('next'):
            return redirect(request.GET.get('next'))
        return redirect('tasks:home')


class TaskDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    """Delete the task"""
    model = Task
    slug_field = 'slug'
    success_url = reverse_lazy("tasks:home")
    template_name = 'tasks/task_confirm_delete.html'

    def get_success_url(self) -> str:
        """Get the page redirect"""
        if self.request.GET.get('next'):
            return self.request.GET.get('next')
        return super().get_success_url()

    def get_success_message(self, cleaned_data: dict[str, Any]) -> str:
        """Success message after delete"""
        return f"Task was deleted: {self.object.name}"


class CategoryCreateView(LoginRequiredMixin, CreateView):
    """Create a new category"""
    model = Category
    form_class = CategoryCreateForm
    success_url = reverse_lazy('tasks:home')
    template_name = 'tasks/add-category.html'

    def form_valid(self, form: CategoryCreateForm) -> HttpResponse:
        """
        Display success message if form is valid.
        Set the user to new category.
        """
        form.instance.user = self.request.user
        messages.success(self.request, f'Category created successfully: {form.instance.name}')
        return super().form_valid(form)


class CategoryDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    """Delete the category"""
    model = Category
    slug_field = 'slug'
    success_url = reverse_lazy("tasks:home")
    template_name = 'tasks/category_confirm_delete.html'

    def get_success_message(self, cleaned_data: dict[str, Any]) -> str:
        """Success message after delete"""
        return f"Category was deleted: {self.object.name}"


class DeleteCompletedView(LoginRequiredMixin, View):
    """Delete all completed tasks"""
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """Process a menu link in a GET request"""
        tasks = Task.objects.filter(is_completed=True, user=self.request.user)
        total_count = tasks.count()
        for task in tasks:
            task.delete()

        if total_count > 0:
            messages.success(request, f'{total_count} completed tasks were deleted')
        else:
            messages.info(request, 'No completed tasks found')
        return redirect('tasks:home')
