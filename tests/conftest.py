import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import app.models  # Import all models to register with Base.metadata
from app.main import app
from app.database.base import Base
from app.database.session import get_db
from app.models.user import User, RoleEnum
from app.auth.security import get_password_hash

# Use in-memory SQLite with StaticPool for fast, isolated, cross-platform tests
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(autouse=True)
def setup_database():
    """Create all tables before each test and drop them after, ensuring complete test isolation."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture
def admin_token(client):
    db = TestingSessionLocal()
    admin_user = User(
        name="Admin",
        email="admin@example.com",
        hashed_password=get_password_hash("adminpass"),
        role=RoleEnum.admin
    )
    db.add(admin_user)
    db.commit()
    db.refresh(admin_user)
    db.close()

    response = client.post(
        "/api/auth/login",
        data={"username": "admin@example.com", "password": "adminpass"}
    )
    return response.json()["access_token"]

@pytest.fixture
def user_token(client):
    client.post(
        "/api/auth/register",
        json={"name": "Task User", "email": "taskuser@example.com", "password": "password123"}
    )
    response = client.post(
        "/api/auth/login",
        data={"username": "taskuser@example.com", "password": "password123"}
    )
    return response.json()["access_token"]

@pytest.fixture
def other_user_token(client):
    client.post(
        "/api/auth/register",
        json={"name": "Other User", "email": "otheruser@example.com", "password": "password123"}
    )
    response = client.post(
        "/api/auth/login",
        data={"username": "otheruser@example.com", "password": "password123"}
    )
    return response.json()["access_token"]
