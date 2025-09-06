from django.urls import path

from .views import TaskDetailView, TaskListView, TaskCreateView, CategoryCreateView, TaskCompleteView, \
    CategoryDeleteView, TaskDeleteView

app_name = 'tasks'

urlpatterns = [
    path('home/', TaskListView.as_view(), name='home'),
    path('tasks/', TaskCreateView.as_view(), name='task-create'),
    path('tasks/<slug:slug>/', TaskDetailView.as_view(), name='task-detail'),
    path('tasks/<slug:slug>/complete', TaskCompleteView.as_view(), name='task-complete'),
    path('tasks/<slug:slug>/delete', TaskDeleteView.as_view(), name='task-delete'),
    path('categories/', CategoryCreateView.as_view(), name='category-create'),
    path('categories/<slug:slug>/', CategoryDeleteView.as_view(), name='category-delete'),
]