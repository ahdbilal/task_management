"""
Task Management API - Main Application
Demo for Admin-Governed Staging Environment
"""
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import os

import crud
import models
import schemas
from database import engine, get_db, init_db

# Initialize database
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Task Management API",
    description="Demo API for Staging Environment with Governance",
    version="1.0.0"
)

# CORS middleware for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_db()

# API Router
from fastapi import APIRouter
api_router = APIRouter(prefix="/api")

# Health check
@api_router.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "environment": "staging"}

# User endpoints
@api_router.post("/users/", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Create a new user"""
    # Check if user exists
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already taken")
    
    return crud.create_user(db=db, user=user)

@api_router.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all users"""
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@api_router.get("/users/{user_id}", response_model=schemas.UserWithTasks)
def read_user(user_id: int, db: Session = Depends(get_db)):
    """Get user by ID with their tasks"""
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Task endpoints
@api_router.post("/users/{user_id}/tasks/", response_model=schemas.Task, status_code=status.HTTP_201_CREATED)
def create_task(user_id: int, task: schemas.TaskCreate, db: Session = Depends(get_db)):
    """Create a new task for a user"""
    db_user = crud.get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return crud.create_task(db=db, task=task, user_id=user_id)

@api_router.get("/tasks/", response_model=List[schemas.Task])
def read_tasks(skip: int = 0, limit: int = 100, user_id: int = None, db: Session = Depends(get_db)):
    """Get all tasks, optionally filtered by user"""
    tasks = crud.get_tasks(db, skip=skip, limit=limit, user_id=user_id)
    return tasks

@api_router.get("/tasks/{task_id}", response_model=schemas.Task)
def read_task(task_id: int, db: Session = Depends(get_db)):
    """Get task by ID"""
    db_task = crud.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@api_router.patch("/tasks/{task_id}", response_model=schemas.Task)
def update_task(task_id: int, task_update: schemas.TaskUpdate, db: Session = Depends(get_db)):
    """Update a task"""
    db_task = crud.update_task(db, task_id=task_id, task_update=task_update)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@api_router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """Delete a task"""
    success = crud.delete_task(db, task_id=task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return None

@api_router.get("/tasks/priority/{priority}", response_model=List[schemas.Task])
def read_tasks_by_priority(priority: str, user_id: int = None, db: Session = Depends(get_db)):
    """Get tasks by priority (low, medium, high)"""
    if priority not in ["low", "medium", "high"]:
        raise HTTPException(status_code=400, detail="Invalid priority. Must be: low, medium, or high")
    
    tasks = crud.get_tasks_by_priority(db, priority=priority, user_id=user_id)
    return tasks

@api_router.get("/stats/completed")
def get_completed_stats(user_id: int = None, db: Session = Depends(get_db)):
    """Get statistics on completed tasks"""
    count = crud.get_completed_tasks_count(db, user_id=user_id)
    return {"completed_tasks": count, "user_id": user_id}

# Include API router
app.include_router(api_router)

# Serve React build (if it exists) - MUST be after API router
if os.path.exists("frontend/build"):
    app.mount("/", StaticFiles(directory="frontend/build", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

