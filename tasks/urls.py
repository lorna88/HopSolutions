from django.urls import path

from .views import TaskDetailView, TaskListView, TaskCreateView

app_name = 'tasks'

urlpatterns = [
    path('home/', TaskListView.as_view(), name='home'),
    path('tasks/create/', TaskCreateView.as_view(), name='task-create'),
    path('tasks/<slug:slug>/', TaskDetailView.as_view(), name='task-detail'),
]