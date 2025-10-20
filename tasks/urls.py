from django.urls import path

from .views import TaskDetailView, TaskListView, TaskCreateView, \
    CategoryCreateView, TaskCompleteView, CategoryDeleteView, TaskDeleteView, \
    DeleteCompletedView, TaskRedirectView

app_name = 'tasks'

urlpatterns = [
    path('home/', TaskListView.as_view(), name='home'),
    path('tasks/', TaskCreateView.as_view(), name='task-create'),
    path('tasks/delete_completed/', DeleteCompletedView.as_view(), name='delete-completed'),
    path('tasks/back/', TaskRedirectView.as_view(), name='back'),
    path('tasks/<int:pk>/complete/', TaskCompleteView.as_view(), name='task-complete'),
    path('tasks/<int:pk>/delete/', TaskDeleteView.as_view(), name='task-delete'),
    path('tasks/<str:username>/<slug:slug>/', TaskDetailView.as_view(), name='task-detail'),
    path('categories/', CategoryCreateView.as_view(), name='category-create'),
    path('categories/<int:pk>/', CategoryDeleteView.as_view(), name='category-delete'),
]
