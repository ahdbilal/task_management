"""
Seed the database with demo data for presentation
"""
from database import SessionLocal, init_db
import crud
import schemas

def seed_database():
    """Create demo users and tasks"""
    db = SessionLocal()
    
    print("🌱 Seeding database with demo data...")
    
    try:
        # Initialize database
        init_db()
        
        # Create demo users
        users_data = [
            {"email": "alice@example.com", "username": "alice", "password": "demo123"},
            {"email": "bob@example.com", "username": "bob", "password": "demo123"},
            {"email": "charlie@example.com", "username": "charlie", "password": "demo123"},
        ]
        
        users = []
        for user_data in users_data:
            # Check if user already exists
            existing = crud.get_user_by_email(db, user_data["email"])
            if not existing:
                user = crud.create_user(db, schemas.UserCreate(**user_data))
                users.append(user)
                print(f"✓ Created user: {user.username}")
            else:
                users.append(existing)
                print(f"  User {existing.username} already exists")
        
        # Create tasks for each user
        tasks_data = {
            "alice": [
                {"title": "Implement user authentication", "description": "Add JWT token-based auth to API", "priority": "high", "completed": True},
                {"title": "Write API documentation", "description": "Document all endpoints with examples", "priority": "medium", "completed": True},
                {"title": "Fix database migration bug", "description": "Users table failing on production", "priority": "high", "completed": False},
                {"title": "Add search functionality", "description": "Implement full-text search for tasks", "priority": "medium", "completed": False},
                {"title": "Update dependencies", "description": "Upgrade React to latest version", "priority": "low", "completed": False},
                {"title": "Design new landing page", "description": "Create mockups for homepage redesign", "priority": "low", "completed": True},
            ],
            "bob": [
                {"title": "Deploy to staging", "description": "Configure Azure VM for staging environment", "priority": "high", "completed": True},
                {"title": "Set up monitoring", "description": "Add DataDog integration for metrics", "priority": "high", "completed": False},
                {"title": "Database backup script", "description": "Automate daily backups to S3", "priority": "medium", "completed": True},
                {"title": "Performance optimization", "description": "Reduce API response time by 50%", "priority": "medium", "completed": False},
                {"title": "Code review process", "description": "Establish team code review guidelines", "priority": "low", "completed": False},
            ],
            "charlie": [
                {"title": "Customer onboarding flow", "description": "Build wizard for new user signup", "priority": "high", "completed": False},
                {"title": "Email notifications", "description": "Send task reminders via email", "priority": "medium", "completed": False},
                {"title": "Dark mode UI", "description": "Implement dark theme for dashboard", "priority": "low", "completed": True},
                {"title": "Mobile responsive design", "description": "Optimize UI for mobile devices", "priority": "medium", "completed": True},
                {"title": "Export to PDF", "description": "Add ability to export tasks as PDF", "priority": "low", "completed": False},
                {"title": "Integration tests", "description": "Write end-to-end test suite", "priority": "high", "completed": True},
                {"title": "Refactor codebase", "description": "Clean up technical debt in auth module", "priority": "medium", "completed": False},
            ],
        }
        
        for user in users:
            if user.username in tasks_data:
                for task_data in tasks_data[user.username]:
                    task = crud.create_task(db, schemas.TaskCreate(**task_data), user.id)
                    status = "✓" if task.completed else "○"
                    priority_emoji = {"high": "🔴", "medium": "🟠", "low": "🟢"}[task.priority]
                    print(f"  {status} {priority_emoji} {task.title} ({user.username})")
        
        print("\n✅ Database seeded successfully!")
        print(f"\n📊 Summary:")
        print(f"  • Users: {len(users)}")
        
        # Count tasks by status
        all_tasks = crud.get_tasks(db, limit=1000)
        completed = len([t for t in all_tasks if t.completed])
        pending = len([t for t in all_tasks if not t.completed])
        
        print(f"  • Total tasks: {len(all_tasks)}")
        print(f"  • Completed: {completed}")
        print(f"  • Pending: {pending}")
        
        # Count by priority
        high = len([t for t in all_tasks if t.priority == "high"])
        medium = len([t for t in all_tasks if t.priority == "medium"])
        low = len([t for t in all_tasks if t.priority == "low"])
        
        print(f"  • High priority: {high}")
        print(f"  • Medium priority: {medium}")
        print(f"  • Low priority: {low}")
        
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()

