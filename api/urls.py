from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api.views import TaskViewSet, CategoryViewSet, TagViewSet, RegisterUserView

app_name = 'api'

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'tags', TagViewSet, basename='tag')

urlpatterns = [
    path('', include(router.urls)),
    path('users/login/', TokenObtainPairView.as_view(), name='login'),
    path('users/login/refresh/', TokenRefreshView.as_view(), name='login_refresh'),
    path('users/register/', RegisterUserView.as_view(), name='register'),
]