from django.test import TestCase
from django.urls import reverse
from .models import Task

class TaskModelTests(TestCase):
    def test_create_task(self):
        """Test creating a new task"""
        task = Task.objects.create(
            title='Test task',
            description='Test description',
            status='todo'
        )
        self.assertEqual(task.title, 'Test task')
        self.assertEqual(task.status, 'todo')

class TaskAPITests(TestCase):
    def test_task_list_view(self):
        """Test task list API endpoint"""
        response = self.client.get(reverse('task-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'tasks')

    def test_task_create_view(self):
        """Test task creation API endpoint"""
        response = self.client.post(reverse('task-create'), {
            'title': 'New task',
            'description': 'Task description',
            'status': 'todo'
        })
        self.assertEqual(response.status_code, 201)
