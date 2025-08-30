from django.urls import path

from tasks.views import TaskDetailView, TaskListView, TaskView

app_name = 'tasks'

urlpatterns = [
    path('home/', TaskView.as_view(), name='home'),
    path('tasks/<slug:slug>/', TaskDetailView.as_view(), name='task-detail'),
]