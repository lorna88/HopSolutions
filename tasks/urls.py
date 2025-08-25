from django.urls import path

from tasks.views import TaskDetailView, TaskListView

app_name = 'tasks'

urlpatterns = [
    path('tasks/<slug:slug>/', TaskDetailView.as_view(), name='task-detail'),
    path('home/', TaskListView.as_view(), name='home'),
]