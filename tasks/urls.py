from django.urls import path

from tasks.views import TaskDetailView

app_name = 'tasks'

urlpatterns = [
    path('tasks/<slug:slug>', TaskDetailView.as_view(), name='task'),
]