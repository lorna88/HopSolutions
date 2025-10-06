from django.urls import path

from .views import MyDayView

app_name = 'calendar'

urlpatterns = [
    path('', MyDayView.as_view(), name='my_day'),
]