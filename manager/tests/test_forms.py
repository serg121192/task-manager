from django.test import TestCase

from manager.forms import WorkerCreateForm
from manager.models import Position


class WorkerCreationFormTest(TestCase):
    def test_new_worker_creation_with_valid_data(self):
        form_data = {
            "username": "test_worker",
            "email": "test_worker@task.manager.com",
            "password1": "Test1234!",
            "password2": "Test1234!",
            "first_name": "Test",
            "last_name": "Worker",
            "position": Position.objects.create(name="Test_position")
        }

        form = WorkerCreateForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
