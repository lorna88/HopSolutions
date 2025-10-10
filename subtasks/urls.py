from django.urls import path

from .views import SubtaskCreateView, SubtaskCompleteView, SubtaskDeleteView

app_name = 'subtasks'

urlpatterns = [
    path('<slug:task_slug>/', SubtaskCreateView.as_view(), name='create'),
    path('<slug:task_slug>/<int:subtask_id>/complete',
         SubtaskCompleteView.as_view(),
         name='complete'),
    path('<slug:task_slug>/<int:subtask_id>/delete', SubtaskDeleteView.as_view(), name='delete'),
]
