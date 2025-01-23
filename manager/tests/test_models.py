from django.contrib.auth import get_user_model
from django.test import TestCase

from manager.models import (
    Position,
    Project,
    TaskType,
    Tag,
    Task,
)


class ModelsTest(TestCase):
    def test_position_str(self):
        position = Position.objects.create(name="Test_position")
        self.assertEqual(str(position), position.name)

    def test_project_str(self):
        project = Project.objects.create(name="Test_project")
        self.assertEqual(str(project), project.name)

    def test_task_type_str(self):
        task_type = TaskType.objects.create(name="Test_type")
        self.assertEqual(str(task_type), task_type.name)

    def test_tag_str(self):
        tag = Tag.objects.create(name="Test_tag")
        self.assertEqual(str(tag), tag.name)

    def test_worker_str(self):
        worker = get_user_model().objects.create_user(
            username="Test_worker",
            email="test_worker@task.manager.com",
            password="Test1234!",
            position=Position.objects.create(name="Test_position"),
        )
        worker_2 = get_user_model().objects.create_user(
            username="Test_worker2",
            email="test_worker2@task.manager.com",
            password="Test1234!",
        )
        worker_3 = get_user_model().objects.create_user(
            username="Test_worker3",
            email="test_worker3@task.manager.com",
            password="Test1234!",
            first_name="Test",
            last_name="Worker3",
        )
        worker_4 = get_user_model().objects.create_user(
            username="Test_worker4",
            email="test_worker4@task.manager.com",
            password="Test1234!",
            first_name="Test",
            last_name="Worker4",
            position=Position.objects.create(name="Test_position4"),
        )

        self.assertEqual(str(worker),
                         f"{worker.username} ({worker.position.name})"
                         )
        self.assertEqual(str(worker_2), worker_2.username)
        self.assertEqual(str(worker_3),
                         f"{worker_3.username} "
                         f"({worker_3.first_name} {worker_3.last_name})"
                         )
        self.assertEqual(str(worker_4),
                         f"{worker_4.username} "
                         f"({worker_4.first_name} {worker_4.last_name}: "
                         f"{worker_4.position.name})"
                         )

    def test_task_str(self):
        task = Task.objects.create(
            name="Test_task",
            task_type=TaskType.objects.create(name="Test_type"),
            priority=3,
        )
        task_2 = Task.objects.create(
            name="Test_task_2",
            task_type=TaskType.objects.create(name="Test_type2"),
        )

        self.assertEqual(str(task), f"{task.name} ({task.priority})")
        self.assertEqual(str(task_2), f"{task_2.name} ({task_2.priority})")
