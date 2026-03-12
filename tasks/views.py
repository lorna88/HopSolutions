from typing import Any

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, UpdateView, CreateView, DeleteView

from tags.models import Tag
from .forms import TaskUpdateForm, CategoryCreateForm
from .models import Task, Category
from .selectors import get_categories
from .services import task_complete, task_create, NonUniqueTaskSlugError, task_delete_completed


class TaskListView(LoginRequiredMixin, ListView):
    """Display the list of categories with its tasks."""
    template_name = 'tasks/home.html'
    model = Category
    context_object_name = 'categories'
    paginate_by = 5

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        """Set parameters into template context"""
        context = super().get_context_data(**kwargs)
        context['all_categories'] = Category.objects.for_user(self.request.user)
        context['tags'] = Tag.objects.for_user(self.request.user)

        context['sort_options'] = [
            {'key': 'date_asc', 'label': 'Date ascending'},
            {'key': 'date_desc', 'label': 'Date descending'},
        ]

        context['form'] = CategoryCreateForm()

        return context

    def get_queryset(self) -> list[Category]:  # type: ignore[override]
        """Filter, search and sort options implementation."""
        return list(get_categories(user=self.request.user,
                                   categories=self.request.GET.get('categories', None),
                                   tags=self.request.GET.get('tags', None),
                                   to_search=self.request.GET.get('q', None),
                                   sort_key=self.request.GET.get('sort', 'date_asc')))


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

    def get_success_url(self) -> str:
        """Get the page redirect"""
        if 'next' in self.request.GET:
            return self.request.GET['next']
        return super().get_success_url()

    def get_queryset(self) -> QuerySet:
        return Task.objects.for_user(self.request.user)


class TaskCompleteView(LoginRequiredMixin, View):
    """Make a task completed or active"""
    def post(self, request: HttpRequest, pk: int, *args, **kwargs) -> HttpResponse:
        """Update task status on form post"""
        task_complete(
            pk=pk,
            is_completed=request.POST.get("is_completed") is not None
        )

        if 'next' in request.GET:
            return redirect(request.GET['next'])
        return redirect('tasks:home')


class TaskCreateView(LoginRequiredMixin, View):
    """Create a new task"""
    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """Create a new task on form post"""
        try:
            task = task_create(
                validate=True,
                user=request.user,
                name=request.POST.get("name"),
                category=request.POST.get("category"),
                date=request.POST.get("date")
            )
            messages.success(request, f'Task created successfully: {task.name}')
        except NonUniqueTaskSlugError as e:
            messages.error(request, e.message)

        if 'next' in request.GET:
            return redirect(request.GET['next'])
        return redirect('tasks:home')


class TaskDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    """Delete the task"""
    model = Task
    success_url = reverse_lazy("tasks:home")

    def get_success_url(self) -> str:
        """Get the page redirect"""
        if 'next' in self.request.GET:
            return self.request.GET['next']
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

    def get_form_kwargs(self):
        """Add the keyword argument user for instantiating the form."""
        form_kwargs = super().get_form_kwargs()
        form_kwargs.update(
            {
                "user": self.request.user,
            }
        )
        return form_kwargs

    def form_valid(self, form: CategoryCreateForm) -> HttpResponse:
        """
        Display success message if form is valid.
        Set the user to new category.
        """
        form.instance.user = self.request.user
        messages.success(self.request, f'Category created successfully: {form.instance.name}')
        return super().form_valid(form)

    def form_invalid(self, form: CategoryCreateForm) -> HttpResponse:
        """Display error message if there are errors when filling out the form"""
        for field, error_list in form.errors.items():
            for error in error_list:
                messages.error(self.request, str(error))
        return redirect('tasks:home')


class CategoryDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    """Delete the category"""
    model = Category
    success_url = reverse_lazy("tasks:home")

    def get_success_message(self, cleaned_data: dict[str, Any]) -> str:
        """Success message after delete"""
        return f"Category was deleted: {self.object.name}"


class DeleteCompletedView(LoginRequiredMixin, View):
    """Delete all completed tasks"""
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """Process a menu link in a GET request"""
        total_count = task_delete_completed(user=request.user)
        if total_count > 0:
            messages.success(request, f'{total_count} completed tasks were deleted')
        else:
            messages.info(request, 'No completed tasks found')
        return redirect('tasks:home')


class TaskRedirectView(LoginRequiredMixin, View):
    """Redirect to previous page on a task card"""
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """Get URL from the query string"""
        if 'next' in request.GET:
            return redirect(request.GET['next'])
        return redirect('tasks:home')
