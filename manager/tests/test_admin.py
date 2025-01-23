from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from manager.models import Position


class TestAdminPage(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            email="admin@task.manager.com",
            password="1qazcde3"
        )
        self.client.force_login(self.admin_user)
        self.worker = get_user_model().objects.create_user(
            username="test_worker",
            email="test_worker@task.manager.com",
            password="Test1234!",
            position=Position.objects.create(name="Test_position")
        )

    def test_worker_position_listed(self):
        """
        Test that the worker's position is listed on admin panel page.
        :return:
        """
        url = reverse("admin:manager_worker_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.worker.position)
