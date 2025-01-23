from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from manager.models import (
    Project,
    Team,
    Worker,
    Position, Task, TaskType, Tag,
)


PROJECTS_URL = reverse("manager:project-list")
TEAMS_URL = reverse("manager:team-list")
WORKERS_URL = reverse("manager:worker-list")
POSITIONS_URL = reverse("manager:position-list")
TASKS_URL = reverse("manager:task-list")
TASK_TYPES_URL = reverse("manager:task-type-list")
TAGS_URL = reverse("manager:tag-list")


PROJECTS_LIST = [
    {"name": "Test_project_1",},
    {"name": "Test_project_2",},
    {"name": "Test_project_3",},
    {"name": "Test_project_4",},
    {"name": "Test_project_5",},
]

TEAMS_LIST = [
    {"name": "Test_team_1",},
    {"name": "Test_team_2",},
    {"name": "Test_team_3",},
    {"name": "Test_team_4",},
    {"name": "Test_team_5",},
]

WORKERS_LIST = [
    {
        "username": "Test_worker_1",
        "email": "test_worker_1@task.manager.com",
        "password": "Test1111!",
    },
    {
        "username": "Test_worker_2",
        "email": "test_worker_2@task.manager.com",
        "password": "Test2222!",
    },
    {
        "username": "Test_worker_3",
        "email": "test_worker_3@task.manager.com",
        "password": "Test3333!",
    },
    {
        "username": "Test_worker_4",
        "email": "test_worker_4@task.manager.com",
        "password": "Test444!",
    },
]

POSITIONS_LIST = [
    {"name": "Test_position_1",},
    {"name": "Test_position_2",},
    {"name": "Test_position_3",},
    {"name": "Test_position_4",},
    {"name": "Test_position_5",},
]

TASKS_LIST = [
    {"name": "Test_task_1",},
    {"name": "Test_task_2",},
    {"name": "Test_task_3",},
    {"name": "Test_task_4",},
    {"name": "Test_task_5",},
]

TASK_TYPES_LIST = [
    {"name": "Test_task_type_1",},
    {"name": "Test_task_type_2",},
    {"name": "Test_task_type_3",},
    {"name": "Test_task_type_4",},
    {"name": "Test_task_type_5",},
]

TAGS_LIST = [
    {"name": "Test_tag_1",},
    {"name": "Test_tag_2",},
    {"name": "Test_tag_3",},
    {"name": "Test_tag_4",},
    {"name": "Test_tag_5",},
]


class PublicTestProjects(TestCase):
    def setUp(self):
        self.client = Client()

    def test_project_list_for_unlogged_users(self):
        response = self.client.get(PROJECTS_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateTestProjects(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            email="test_user@task.manager.com",
            password="Test1234!",
        )
        self.client.force_login(self.user)

    def test_project_list_for_logged_users(self):
        for project in PROJECTS_LIST:
            Project.objects.create(**project)

        response = self.client.get(PROJECTS_URL)
        self.assertEqual(response.status_code, 200)
        projects = Project.objects.all()
        search_project_name = "2"
        filtered_projects = Project.objects.filter(
            name__icontains=search_project_name
        )
        filtered_response = self.client.get(
            PROJECTS_URL,
            {
                "name": search_project_name,
            }
        )
        self.assertEqual(
            list(projects),
            list(response.context["projects"]),
        )
        self.assertTemplateUsed(response, "manager/project_list.html")
        self.assertEqual(
            list(filtered_projects),
            list(filtered_response.context["projects"]),
        )
        self.assertEqual(
            filtered_response.context["search_form"].initial["name"],
            search_project_name,
        )


class PublicTestTeams(TestCase):
    def setUp(self):
        self.client = Client()

    def test_teams_list_for_unlogged_users(self):
        response = self.client.get(TEAMS_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateTestTeams(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            email="test_user@task.manager.com",
            password="Test1234!",
        )
        self.client.force_login(self.user)

    def test_teams_list_for_logged_users(self):
        for team in TEAMS_LIST:
            Team.objects.create(**team)

        response = self.client.get(TEAMS_URL)
        self.assertEqual(response.status_code, 200)
        teams = Team.objects.all()
        search_team_name = "4"
        filtered_teams = Team.objects.filter(
            name__icontains=search_team_name
        )
        filtered_response = self.client.get(
            TEAMS_URL,
            {
                "name": search_team_name,
            }
        )
        self.assertEqual(
            list(teams),
            list(response.context["teams"]),
        )
        self.assertEqual(
            list(filtered_teams),
            list(filtered_response.context["teams"]),
        )
        self.assertEqual(
            filtered_response.context["search_form"].initial["name"],
            search_team_name,
        )
        self.assertTemplateUsed(response, "manager/team_list.html")


class PublicTestWorkers(TestCase):
    def setUp(self):
        self.client = Client()

    def test_workers_list_for_unlogged_users(self):
        response = self.client.get(WORKERS_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateTestWorkers(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            email="test_user@task.manager.com",
            password="Test1234!",
        )
        self.client.force_login(self.user)

    def test_workers_list_for_logged_users(self):
        for worker in WORKERS_LIST:
            Worker.objects.create(**worker)

        response = self.client.get(WORKERS_URL)
        self.assertEqual(response.status_code, 200)
        workers = Worker.objects.all()
        search_worker_username = "3"
        filtered_workers = Worker.objects.filter(
            username__icontains=search_worker_username
        )
        filtered_response = self.client.get(
            WORKERS_URL,
            {
                "username": search_worker_username,
            }
        )
        self.assertEqual(
            list(workers),
            list(response.context["workers"]),
        )
        self.assertEqual(
            list(filtered_workers),
            list(filtered_response.context["workers"]),
        )
        self.assertEqual(
            filtered_response.context["search_form"].initial["username"],
            search_worker_username,
        )
        self.assertTemplateUsed(response, "manager/worker_list.html")


class PublicTestPositions(TestCase):
    def setUp(self):
        self.client = Client()

    def test_positions_list_for_unlogged_users(self):
        response = self.client.get(POSITIONS_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateTestPositions(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            email="test_user@task.manager.com",
            password="Test1234!",
        )
        self.client.force_login(self.user)

    def test_positions_list_for_logged_users(self):
        for position in POSITIONS_LIST:
            Position.objects.create(**position)

        response = self.client.get(POSITIONS_URL)
        self.assertEqual(response.status_code, 200)
        positions = Position.objects.all()
        search_position_name = "5"
        filtered_positions = Position.objects.filter(
            name__icontains=search_position_name
        )
        filtered_response = self.client.get(
            POSITIONS_URL,
            {
                "name": search_position_name,
            }
        )
        self.assertEqual(
            list(positions),
            list(response.context["positions"]),
        )
        self.assertEqual(
            list(filtered_positions),
            list(filtered_response.context["positions"]),
        )
        self.assertEqual(
            filtered_response.context["search_form"].initial["name"],
            search_position_name,
        )
        self.assertTemplateUsed(response, "manager/position_list.html")


class PublicTestTasks(TestCase):
    def setUp(self):
        self.client = Client()

    def test_tasks_list_for_unlogged_users(self):
        response = self.client.get(TASKS_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateTestTasks(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            email="test_user@task.manager.com",
            password="Test1234!",
        )
        self.client.force_login(self.user)

    def test_tasks_list_for_logged_users(self):
        for task in TASKS_LIST:
            Task.objects.create(**task)

        response = self.client.get(TASKS_URL)
        self.assertEqual(response.status_code, 200)
        tasks = Task.objects.all()
        search_task_name = "1"
        filtered_tasks = Task.objects.filter(
            name__icontains=search_task_name
        )
        filtered_response = self.client.get(
            TASKS_URL,
            {
                "name": search_task_name,
            }
        )
        self.assertEqual(
            list(tasks),
            list(response.context["tasks"]),
        )
        self.assertEqual(
            list(filtered_tasks),
            list(filtered_response.context["tasks"]),
        )
        self.assertEqual(
            filtered_response.context["search_form"].initial["name"],
            search_task_name,
        )
        self.assertTemplateUsed(response, "manager/task_list.html")


class PublicTestTaskTypes(TestCase):
    def setUp(self):
        self.client = Client()

    def test_tasks_list_for_unlogged_users(self):
        response = self.client.get(TASKS_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateTestTaskTypes(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            email="test_user@task.manager.com",
            password="Test1234!",
        )
        self.client.force_login(self.user)

    def test_tasks_list_for_logged_users(self):
        response = self.client.get(TASKS_URL)
        self.assertNotEqual(response.status_code, 200)
        task_types = TaskType.objects.all()
        search_task_type_name = "2"
        filtered_task_types = TaskType.objects.filter(
            name__icontains=search_task_type_name
        )
        filtered_response = self.client.get(
            TASKS_URL,
            {
                "name": search_task_type_name,
            }
        )
        self.assertEqual(
            list(task_types),
            list(response.context["task_types"]),
        )
        self.assertEqual(
            list(filtered_task_types),
            list(filtered_response.context["task_types"]),
        )
        self.assertEqual(
            filtered_response.context["search_form"].initial["name"],
            search_task_type_name,
        )
        self.assertTemplateUsed(response, "manager/task_list.html")


class PublicTestTags(TestCase):
    def setUp(self):
        self.client = Client()

    def test_tags_list_for_unlogged_users(self):
        response = self.client.get(TAGS_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateTestTags(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            email="test_user@task.manager.com",
            password="Test1234!",
        )
        self.client.force_login(self.user)

    def test_tags_list_for_logged_users(self):
        response = self.client.get(TAGS_URL)
        self.assertNotEqual(response.status_code, 200)
        tags = Tag.objects.all()
        search_tag_name = "3"
        filtered_tags = Tag.objects.filter(
            name__icontains=search_tag_name
        )
        filtered_response = self.client.get(
            TAGS_URL,
            {
                "name": search_tag_name,
            }
        )
        self.assertEqual(
            list(tags),
            list(response.context["tags"]),
        )
        self.assertEqual(
            list(filtered_tags),
            list(filtered_response.context["tags"]),
        )
        self.assertEqual(
            filtered_response.context["search_form"].initial["name"],
            search_tag_name,
        )
        self.assertTemplateUsed(response, "manager/tags_list.html")
