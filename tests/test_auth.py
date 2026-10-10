import pytest

def test_register_success(client):
    response = client.post(
        "/api/auth/register",
        json={"name": "Test User", "email": "test@example.com", "password": "password123"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test User"
    assert data["email"] == "test@example.com"
    assert data["role"] == "user"
    assert "password" not in data
    assert "hashed_password" not in data

def test_register_duplicate(client):
    # First registration
    client.post(
        "/api/auth/register",
        json={"name": "Test User", "email": "duplicate@example.com", "password": "password123"}
    )
    # Duplicate registration attempt
    response = client.post(
        "/api/auth/register",
        json={"name": "Test User 2", "email": "duplicate@example.com", "password": "password123"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

def test_register_invalid_email(client):
    response = client.post(
        "/api/auth/register",
        json={"name": "Bad Email", "email": "not-an-email", "password": "password123"}
    )
    assert response.status_code == 422

def test_register_short_password(client):
    response = client.post(
        "/api/auth/register",
        json={"name": "Short Pass", "email": "short@example.com", "password": "short"}
    )
    assert response.status_code == 422

def test_login_success(client):
    client.post(
        "/api/auth/register",
        json={"name": "Login User", "email": "login@example.com", "password": "password123"}
    )
    response = client.post(
        "/api/auth/login",
        data={"username": "login@example.com", "password": "password123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_incorrect_password(client):
    client.post(
        "/api/auth/register",
        json={"name": "Login User", "email": "login@example.com", "password": "password123"}
    )
    response = client.post(
        "/api/auth/login",
        data={"username": "login@example.com", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password"

def test_login_nonexistent_user(client):
    response = client.post(
        "/api/auth/login",
        data={"username": "nonexistent@example.com", "password": "password123"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password"

def test_protected_access_without_token(client):
    response = client.get("/api/auth/me")
    assert response.status_code == 401

def test_protected_access_with_valid_token(client):
    client.post(
        "/api/auth/register",
        json={"name": "Me User", "email": "me@example.com", "password": "password123"}
    )
    login_res = client.post(
        "/api/auth/login",
        data={"username": "me@example.com", "password": "password123"}
    )
    token = login_res.json()["access_token"]
    response = client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "me@example.com"
    assert data["name"] == "Me User"

def test_protected_access_with_invalid_jwt(client):
    response = client.get(
        "/api/auth/me",
        headers={"Authorization": "Bearer invalid.token.value"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"

def test_protected_access_with_malformed_header(client):
    response = client.get(
        "/api/auth/me",
        headers={"Authorization": "NotBearerToken"}
    )
    assert response.status_code == 401
