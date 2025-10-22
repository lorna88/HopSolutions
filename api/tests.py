from django.test import TestCase
from rest_framework.test import APIClient

from tasks.models import Category
from users.models import User


class PermissionTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="password", email="test@example.com")
        self.category = Category.objects.create(name="Test Category", slug="test-category", user=self.user)

    def test_owner_permission(self):
        self.client.force_authenticate(user=self.user)
        task_data = {
            'name': 'Test Task',
            'slug': 'test-task',
            'category': 'test-category',
        }
        response = self.client.post(f"/api/tasks/", task_data, format='json')
        self.assertEqual(response.status_code, 201)
