import pytest
import sys
import os
from flask import json

# Add parent directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app

@pytest.fixture(name="test_client")
def fixture_test_client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_tasks(test_client):
    """Test getting all tasks"""
    response = client.get('/api/tasks')
    assert response.status_code == 200
    assert isinstance(json.loads(response.data), list)

def test_create_task(test_client):
    """Test creating a new task"""
    task_data = {
        'title': 'Test Task',
        'description': 'Test Description',
        'status': 'todo'
    }
    response = client.post('/api/tasks', 
        data=json.dumps(task_data),
        content_type='application/json'
    )
    assert response.status_code == 201
    assert b'Test Task' in response.data

def test_update_task(test_client):
    """Test updating a task"""
    # First create a task to update
    task_data = {'title': 'Original Task'}
    response = client.post('/api/tasks', 
        data=json.dumps(task_data),
        content_type='application/json'
    )
    task_id = json.loads(response.data)['id']
    
    # Update the task
    updated_data = {'title': 'Updated Task'}
    response = client.put(f'/api/tasks/{task_id}',
        data=json.dumps(updated_data),
        content_type='application/json'
    )
    assert response.status_code == 200
    assert b'Updated Task' in response.data

def test_delete_task(test_client):
    """Test deleting a task"""
    # First create a task to delete
    task_data = {'title': 'Task to Delete'}
    response = client.post('/api/tasks', 
        data=json.dumps(task_data),
        content_type='application/json'
    )
    task_id = json.loads(response.data)['id']
    
    # Delete the task
    response = client.delete(f'/api/tasks/{task_id}')
    assert response.status_code == 204
