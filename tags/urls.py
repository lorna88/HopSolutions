from django.urls import path

from .views import TagView

app_name = 'tags'

urlpatterns = [
    path('<int:task_id>/', TagView.as_view(), name='tag-list'),
]
