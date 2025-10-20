"""
Integration tests for API endpoints
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, get_db
from main import app

# Test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_api.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client():
    """Create test client with fresh database"""
    Base.metadata.create_all(bind=engine)
    client = TestClient(app)
    yield client
    Base.metadata.drop_all(bind=engine)

def test_health_check(client):
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "environment": "staging"}

def test_create_user_success(client):
    """Test successful user creation"""
    response = client.post(
        "/users/",
        json={
            "email": "newuser@example.com",
            "username": "newuser",
            "password": "securepass123"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert data["username"] == "newuser"
    assert "id" in data
    assert data["is_active"] == True

def test_create_user_duplicate_email(client):
    """Test that duplicate emails are rejected"""
    user_data = {
        "email": "duplicate@example.com",
        "username": "user1",
        "password": "password"
    }
    
    # Create first user
    response1 = client.post("/users/", json=user_data)
    assert response1.status_code == 201
    
    # Try to create user with same email
    user_data["username"] = "user2"
    response2 = client.post("/users/", json=user_data)
    assert response2.status_code == 400
    assert "Email already registered" in response2.json()["detail"]

def test_get_users(client):
    """Test getting list of users"""
    # Create some users
    client.post("/users/", json={"email": "user1@test.com", "username": "user1", "password": "pass"})
    client.post("/users/", json={"email": "user2@test.com", "username": "user2", "password": "pass"})
    
    # Get users
    response = client.get("/users/")
    assert response.status_code == 200
    users = response.json()
    assert len(users) == 2

def test_get_user_by_id(client):
    """Test getting user by ID"""
    # Create user
    create_response = client.post(
        "/users/",
        json={"email": "getme@test.com", "username": "getme", "password": "pass"}
    )
    user_id = create_response.json()["id"]
    
    # Get user
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id
    assert data["email"] == "getme@test.com"
    assert "tasks" in data

def test_get_nonexistent_user(client):
    """Test getting user that doesn't exist"""
    response = client.get("/users/9999")
    assert response.status_code == 404

def test_create_task_for_user(client):
    """Test creating a task for a user"""
    # Create user
    user_response = client.post(
        "/users/",
        json={"email": "taskowner@test.com", "username": "taskowner", "password": "pass"}
    )
    user_id = user_response.json()["id"]
    
    # Create task
    task_response = client.post(
        f"/users/{user_id}/tasks/",
        json={
            "title": "My First Task",
            "description": "This is a test task",
            "priority": "high"
        }
    )
    assert task_response.status_code == 201
    task_data = task_response.json()
    assert task_data["title"] == "My First Task"
    assert task_data["priority"] == "high"
    assert task_data["completed"] == False
    assert task_data["owner_id"] == user_id

def test_get_all_tasks(client):
    """Test getting all tasks"""
    # Create user and tasks
    user_response = client.post(
        "/users/",
        json={"email": "multi@test.com", "username": "multi", "password": "pass"}
    )
    user_id = user_response.json()["id"]
    
    client.post(f"/users/{user_id}/tasks/", json={"title": "Task 1"})
    client.post(f"/users/{user_id}/tasks/", json={"title": "Task 2"})
    
    # Get all tasks
    response = client.get("/tasks/")
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 2

def test_update_task(client):
    """Test updating a task"""
    # Create user and task
    user_response = client.post(
        "/users/",
        json={"email": "updater@test.com", "username": "updater", "password": "pass"}
    )
    user_id = user_response.json()["id"]
    
    task_response = client.post(
        f"/users/{user_id}/tasks/",
        json={"title": "Original", "priority": "low"}
    )
    task_id = task_response.json()["id"]
    
    # Update task
    update_response = client.patch(
        f"/tasks/{task_id}",
        json={"title": "Updated", "completed": True}
    )
    assert update_response.status_code == 200
    updated = update_response.json()
    assert updated["title"] == "Updated"
    assert updated["completed"] == True
    assert updated["priority"] == "low"  # Unchanged

def test_delete_task(client):
    """Test deleting a task"""
    # Create user and task
    user_response = client.post(
        "/users/",
        json={"email": "deleter@test.com", "username": "deleter", "password": "pass"}
    )
    user_id = user_response.json()["id"]
    
    task_response = client.post(
        f"/users/{user_id}/tasks/",
        json={"title": "To Delete"}
    )
    task_id = task_response.json()["id"]
    
    # Delete task
    delete_response = client.delete(f"/tasks/{task_id}")
    assert delete_response.status_code == 204
    
    # Verify task is gone
    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 404

def test_get_tasks_by_priority(client):
    """Test filtering tasks by priority"""
    # Create user and tasks
    user_response = client.post(
        "/users/",
        json={"email": "priority@test.com", "username": "priority", "password": "pass"}
    )
    user_id = user_response.json()["id"]
    
    client.post(f"/users/{user_id}/tasks/", json={"title": "High1", "priority": "high"})
    client.post(f"/users/{user_id}/tasks/", json={"title": "High2", "priority": "high"})
    client.post(f"/users/{user_id}/tasks/", json={"title": "Low1", "priority": "low"})
    
    # Get high priority tasks
    response = client.get("/tasks/priority/high")
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 2
    assert all(task["priority"] == "high" for task in tasks)

def test_get_tasks_invalid_priority(client):
    """Test that invalid priority returns error"""
    response = client.get("/tasks/priority/invalid")
    assert response.status_code == 400
    assert "Invalid priority" in response.json()["detail"]

def test_completed_stats(client):
    """Test completed tasks statistics"""
    # Create user and tasks
    user_response = client.post(
        "/users/",
        json={"email": "stats@test.com", "username": "stats", "password": "pass"}
    )
    user_id = user_response.json()["id"]
    
    # Create tasks
    task1_resp = client.post(f"/users/{user_id}/tasks/", json={"title": "Task1"})
    task2_resp = client.post(f"/users/{user_id}/tasks/", json={"title": "Task2"})
    task3_resp = client.post(f"/users/{user_id}/tasks/", json={"title": "Task3"})
    
    # Complete some tasks
    client.patch(f"/tasks/{task1_resp.json()['id']}", json={"completed": True})
    client.patch(f"/tasks/{task2_resp.json()['id']}", json={"completed": True})
    
    # Get stats
    response = client.get(f"/stats/completed?user_id={user_id}")
    assert response.status_code == 200
    stats = response.json()
    assert stats["completed_tasks"] == 2
    assert stats["user_id"] == user_id

