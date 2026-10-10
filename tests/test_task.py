import pytest

def test_create_task(client, user_token):
    response = client.post(
        "/api/tasks",
        headers={"Authorization": f"Bearer {user_token}"},
        json={"title": "Test Task", "description": "Desc"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "Desc"
    assert data["status"] == "Pending"
    assert "id" in data

def test_create_task_whitespace_title(client, user_token):
    response = client.post(
        "/api/tasks",
        headers={"Authorization": f"Bearer {user_token}"},
        json={"title": "   ", "description": "Desc"}
    )
    assert response.status_code == 422

def test_list_tasks_user(client, user_token):
    client.post(
        "/api/tasks",
        headers={"Authorization": f"Bearer {user_token}"},
        json={"title": "User Task 1", "description": "Desc 1"}
    )
    response = client.get(
        "/api/tasks",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 1
    assert tasks[0]["title"] == "User Task 1"

def test_list_tasks_admin_sees_all(client, admin_token, user_token):
    client.post(
        "/api/tasks",
        headers={"Authorization": f"Bearer {user_token}"},
        json={"title": "User Task For Admin Check", "description": "Desc"}
    )
    # Admin list tasks should see the user's task
    response = client.get(
        "/api/tasks",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) >= 1
    titles = [t["title"] for t in tasks]
    assert "User Task For Admin Check" in titles

def test_get_task_by_id_owner(client, user_token):
    create_res = client.post(
        "/api/tasks",
        headers={"Authorization": f"Bearer {user_token}"},
        json={"title": "Fetchable Task", "description": "Desc"}
    )
    task_id = create_res.json()["id"]

    response = client.get(
        f"/api/tasks/{task_id}",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 200
    assert response.json()["id"] == task_id
    assert response.json()["title"] == "Fetchable Task"

def test_get_task_by_id_admin(client, admin_token, user_token):
    create_res = client.post(
        "/api/tasks",
        headers={"Authorization": f"Bearer {user_token}"},
        json={"title": "User Task for Admin Retrieval", "description": "Desc"}
    )
    task_id = create_res.json()["id"]

    response = client.get(
        f"/api/tasks/{task_id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    assert response.json()["id"] == task_id

def test_get_task_by_id_forbidden(client, other_user_token, user_token):
    create_res = client.post(
        "/api/tasks",
        headers={"Authorization": f"Bearer {user_token}"},
        json={"title": "Private Task", "description": "Desc"}
    )
    task_id = create_res.json()["id"]

    response = client.get(
        f"/api/tasks/{task_id}",
        headers={"Authorization": f"Bearer {other_user_token}"}
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Not enough permissions"

def test_get_task_by_id_not_found(client, user_token):
    response = client.get(
        "/api/tasks/99999",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"

def test_edit_task_success(client, user_token):
    create_res = client.post(
        "/api/tasks",
        headers={"Authorization": f"Bearer {user_token}"},
        json={"title": "Original Title", "description": "Original Desc"}
    )
    task_id = create_res.json()["id"]

    response = client.patch(
        f"/api/tasks/{task_id}",
        headers={"Authorization": f"Bearer {user_token}"},
        json={"title": "Updated Title", "description": "Updated Desc"}
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Title"
    assert response.json()["description"] == "Updated Desc"

def test_edit_task_admin(client, admin_token, user_token):
    create_res = client.post(
        "/api/tasks",
        headers={"Authorization": f"Bearer {user_token}"},
        json={"title": "User Title", "description": "User Desc"}
    )
    task_id = create_res.json()["id"]

    response = client.patch(
        f"/api/tasks/{task_id}",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"title": "Admin Edited Title"}
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Admin Edited Title"

def test_edit_task_forbidden(client, other_user_token, user_token):
    create_res = client.post(
        "/api/tasks",
        headers={"Authorization": f"Bearer {user_token}"},
        json={"title": "User Title", "description": "User Desc"}
    )
    task_id = create_res.json()["id"]

    response = client.patch(
        f"/api/tasks/{task_id}",
        headers={"Authorization": f"Bearer {other_user_token}"},
        json={"title": "Hacked Title"}
    )
    assert response.status_code == 403

def test_edit_task_not_found(client, user_token):
    response = client.patch(
        "/api/tasks/99999",
        headers={"Authorization": f"Bearer {user_token}"},
        json={"title": "Non-existent"}
    )
    assert response.status_code == 404

def test_admin_update_status_all_statuses(client, admin_token, user_token):
    create_res = client.post(
        "/api/tasks",
        headers={"Authorization": f"Bearer {user_token}"},
        json={"title": "Status Test Task", "description": "Desc"}
    )
    task_id = create_res.json()["id"]

    # Verify each allowed status
    for status_value in ["In Progress", "Testing", "Completed", "Pending"]:
        response = client.patch(
            f"/api/tasks/{task_id}/status",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={"status": status_value}
        )
        assert response.status_code == 200
        assert response.json()["status"] == status_value

def test_user_update_status_forbidden(client, user_token):
    create_res = client.post(
        "/api/tasks",
        headers={"Authorization": f"Bearer {user_token}"},
        json={"title": "Status Test Task", "description": "Desc"}
    )
    task_id = create_res.json()["id"]

    response = client.patch(
        f"/api/tasks/{task_id}/status",
        headers={"Authorization": f"Bearer {user_token}"},
        json={"status": "Testing"}
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Not enough permissions"

def test_update_status_invalid_value(client, admin_token, user_token):
    create_res = client.post(
        "/api/tasks",
        headers={"Authorization": f"Bearer {user_token}"},
        json={"title": "Status Test Task", "description": "Desc"}
    )
    task_id = create_res.json()["id"]

    response = client.patch(
        f"/api/tasks/{task_id}/status",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"status": "Archived"}
    )
    assert response.status_code == 422

def test_update_status_not_found(client, admin_token):
    response = client.patch(
        "/api/tasks/99999/status",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"status": "Completed"}
    )
    assert response.status_code == 404

def test_unauthenticated_access(client):
    response = client.get("/api/tasks")
    assert response.status_code == 401
