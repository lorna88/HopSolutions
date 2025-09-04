from django.urls import path

from .views import TaskDetailView, TaskListView, TaskCreateView, CategoryCreateView

app_name = 'tasks'

urlpatterns = [
    path('home/', TaskListView.as_view(), name='home'),
    path('tasks/', TaskCreateView.as_view(), name='task-create'),
    path('tasks/<slug:slug>/', TaskDetailView.as_view(), name='task-detail'),
    path('categories/', CategoryCreateView.as_view(), name='category-create'),
]