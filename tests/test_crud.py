"""
Unit tests for CRUD operations
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base
import crud
import schemas
import models

# Test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def db():
    """Create a fresh database for each test"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

def test_create_user(db):
    """Test creating a user"""
    user_data = schemas.UserCreate(
        email="test@example.com",
        username="testuser",
        password="securepassword"
    )
    user = crud.create_user(db, user_data)
    
    assert user.email == "test@example.com"
    assert user.username == "testuser"
    assert user.is_active == True
    assert user.id is not None

def test_get_user_by_email(db):
    """Test retrieving user by email"""
    user_data = schemas.UserCreate(
        email="test@example.com",
        username="testuser",
        password="password123"
    )
    created_user = crud.create_user(db, user_data)
    
    retrieved_user = crud.get_user_by_email(db, "test@example.com")
    assert retrieved_user is not None
    assert retrieved_user.id == created_user.id
    assert retrieved_user.email == "test@example.com"

def test_password_hashing(db):
    """Test that passwords are hashed correctly"""
    user_data = schemas.UserCreate(
        email="secure@example.com",
        username="secureuser",
        password="mypassword"
    )
    user = crud.create_user(db, user_data)
    
    # Password should be hashed, not plain text
    assert user.hashed_password != "mypassword"
    
    # Should be able to verify password
    assert crud.verify_password("mypassword", user.hashed_password) == True
    assert crud.verify_password("wrongpassword", user.hashed_password) == False

def test_create_task(db):
    """Test creating a task"""
    # Create user first
    user_data = schemas.UserCreate(
        email="taskuser@example.com",
        username="taskuser",
        password="password"
    )
    user = crud.create_user(db, user_data)
    
    # Create task
    task_data = schemas.TaskCreate(
        title="Test Task",
        description="This is a test task",
        priority="high"
    )
    task = crud.create_task(db, task_data, user_id=user.id)
    
    assert task.title == "Test Task"
    assert task.description == "This is a test task"
    assert task.priority == "high"
    assert task.completed == False
    assert task.owner_id == user.id

def test_get_tasks_by_user(db):
    """Test getting tasks filtered by user"""
    # Create two users
    user1 = crud.create_user(db, schemas.UserCreate(
        email="user1@example.com", username="user1", password="pass"
    ))
    user2 = crud.create_user(db, schemas.UserCreate(
        email="user2@example.com", username="user2", password="pass"
    ))
    
    # Create tasks for each user
    crud.create_task(db, schemas.TaskCreate(title="User1 Task1"), user1.id)
    crud.create_task(db, schemas.TaskCreate(title="User1 Task2"), user1.id)
    crud.create_task(db, schemas.TaskCreate(title="User2 Task1"), user2.id)
    
    # Get tasks for user1
    user1_tasks = crud.get_tasks(db, user_id=user1.id)
    assert len(user1_tasks) == 2
    assert all(task.owner_id == user1.id for task in user1_tasks)
    
    # Get tasks for user2
    user2_tasks = crud.get_tasks(db, user_id=user2.id)
    assert len(user2_tasks) == 1
    assert user2_tasks[0].owner_id == user2.id

def test_update_task(db):
    """Test updating a task"""
    user = crud.create_user(db, schemas.UserCreate(
        email="update@example.com", username="updater", password="pass"
    ))
    task = crud.create_task(db, schemas.TaskCreate(title="Original Title"), user.id)
    
    # Update task
    update_data = schemas.TaskUpdate(title="Updated Title", completed=True)
    updated_task = crud.update_task(db, task.id, update_data)
    
    assert updated_task.title == "Updated Title"
    assert updated_task.completed == True
    assert updated_task.priority == "medium"  # Should remain unchanged

def test_delete_task(db):
    """Test deleting a task"""
    user = crud.create_user(db, schemas.UserCreate(
        email="delete@example.com", username="deleter", password="pass"
    ))
    task = crud.create_task(db, schemas.TaskCreate(title="To Delete"), user.id)
    
    # Delete task
    success = crud.delete_task(db, task.id)
    assert success == True
    
    # Verify task is gone
    deleted_task = crud.get_task(db, task.id)
    assert deleted_task is None

def test_get_tasks_by_priority(db):
    """Test filtering tasks by priority"""
    user = crud.create_user(db, schemas.UserCreate(
        email="priority@example.com", username="prioritizer", password="pass"
    ))
    
    # Create tasks with different priorities
    crud.create_task(db, schemas.TaskCreate(title="High1", priority="high"), user.id)
    crud.create_task(db, schemas.TaskCreate(title="High2", priority="high"), user.id)
    crud.create_task(db, schemas.TaskCreate(title="Low1", priority="low"), user.id)
    
    # Get high priority tasks
    high_tasks = crud.get_tasks_by_priority(db, "high")
    assert len(high_tasks) == 2
    assert all(task.priority == "high" for task in high_tasks)

def test_completed_tasks_count(db):
    """Test counting completed tasks"""
    user = crud.create_user(db, schemas.UserCreate(
        email="counter@example.com", username="counter", password="pass"
    ))
    
    # Create tasks (some completed)
    task1 = crud.create_task(db, schemas.TaskCreate(title="Task1"), user.id)
    task2 = crud.create_task(db, schemas.TaskCreate(title="Task2"), user.id)
    task3 = crud.create_task(db, schemas.TaskCreate(title="Task3"), user.id)
    
    # Complete some tasks
    crud.update_task(db, task1.id, schemas.TaskUpdate(completed=True))
    crud.update_task(db, task2.id, schemas.TaskUpdate(completed=True))
    
    # Count completed tasks
    count = crud.get_completed_tasks_count(db, user_id=user.id)
    assert count == 2


