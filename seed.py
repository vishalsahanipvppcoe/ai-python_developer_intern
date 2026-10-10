import os
from sqlalchemy.orm import Session
from app.database.session import engine, SessionLocal
from app.models.user import User, RoleEnum
from app.models.task import Task, StatusEnum
from app.auth.security import get_password_hash
from app.database.base import Base

def seed_database():
    print("Seeding database...")
    
    # Optional: If you want the seeder to create tables without Alembic (for testing)
    # Base.metadata.create_all(bind=engine)
    
    db: Session = SessionLocal()
    
    # 1. Create Admin User
    admin_email = "admin@example.com"
    admin_user = db.query(User).filter(User.email == admin_email).first()
    if not admin_user:
        admin_user = User(
            name="System Admin",
            email=admin_email,
            hashed_password=get_password_hash("admin123"),
            role=RoleEnum.admin
        )
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        print(f"Created Admin user: {admin_email} (Password: admin123)")
    else:
        print(f"Admin user {admin_email} already exists.")

    # 2. Create Regular User
    regular_email = "user@example.com"
    regular_user = db.query(User).filter(User.email == regular_email).first()
    if not regular_user:
        regular_user = User(
            name="Regular User",
            email=regular_email,
            hashed_password=get_password_hash("user123"),
            role=RoleEnum.user
        )
        db.add(regular_user)
        db.commit()
        db.refresh(regular_user)
        print(f"Created Regular user: {regular_email} (Password: user123)")
    else:
        print(f"Regular user {regular_email} already exists.")

    # 3. Create Sample Tasks
    if db.query(Task).count() == 0:
        sample_tasks = [
            Task(
                user_id=admin_user.id,
                title="Review project architecture",
                description="Review the database schema and API design for the AI Task Manager.",
                status=StatusEnum.completed
            ),
            Task(
                user_id=regular_user.id,
                title="Integrate Gemini AI",
                description="Write the integration code for Google Gemini 1.5 Flash.",
                status=StatusEnum.in_progress
            ),
            Task(
                user_id=regular_user.id,
                title="Write Unit Tests",
                description="Ensure test coverage for RBAC and endpoints.",
                status=StatusEnum.pending
            )
        ]
        db.add_all(sample_tasks)
        db.commit()
        print("Created sample tasks.")
    else:
        print("Tasks already exist. Skipping task seeding.")

    db.close()
    print("Database seeding complete!")

if __name__ == "__main__":
    seed_database()
