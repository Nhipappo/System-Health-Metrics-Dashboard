import uuid

import pytest
import requests

BASE_URL = "http://localhost:8000"


def test_create_task():
    payload = {"payload": {"url": "https://api.example.com/data", "method": "GET"}}
    response = requests.post(f"{BASE_URL}/tasks/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "task_id" in data
    task_id = data["task_id"]
    uuid.UUID(task_id, version=4)  # проверка, что это UUID
    # не возвращаем ничего (убрать return)


def test_create_task_empty_payload():
    # FastAPI/Pydantic возвращает 422 при неверных данных
    response = requests.post(f"{BASE_URL}/tasks/", json={"payload": None})
    assert response.status_code == 422


def test_get_task_by_id():
    # создаём задачу
    create_resp = requests.post(
        f"{BASE_URL}/tasks/", json={"payload": {"some_field": "some_value"}}
    )
    assert create_resp.status_code == 200
    task_id = create_resp.json()["task_id"]

    # получаем задачу
    get_resp = requests.get(f"{BASE_URL}/tasks/{task_id}")
    assert get_resp.status_code == 200
    task = get_resp.json()
    assert task["id"] == task_id
    assert task["status"] == "pending"
    # если в TaskResponse есть payload, проверяем его, иначе пропускаем
    if "payload" in task:
        assert task["payload"] == {"some_field": "some_value"}


def test_get_task_not_found():
    random_uuid = str(uuid.uuid4())
    response = requests.get(f"{BASE_URL}/tasks/{random_uuid}")
    assert response.status_code == 404
    assert "not found" in response.text.lower()


def test_get_tasks_list_default():
    response = requests.get(f"{BASE_URL}/tasks/")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert "limit" in data
    assert "offset" in data
    assert isinstance(data["items"], list)


def test_get_tasks_with_pagination():
    # добавим 3 задачи
    for i in range(3):
        requests.post(f"{BASE_URL}/tasks/", json={"payload": {"idx": i}})
    response = requests.get(f"{BASE_URL}/tasks/?limit=2&offset=1")
    assert response.status_code == 200
    data = response.json()
    assert data["limit"] == 2
    assert data["offset"] == 1
    assert len(data["items"]) <= 2


def test_get_tasks_filter_by_status():
    # создадим задачу со статусом pending (по умолчанию)
    requests.post(f"{BASE_URL}/tasks/", json={"payload": {"test": True}})
    response = requests.get(f"{BASE_URL}/tasks/?status=pending")
    assert response.status_code == 200
    data = response.json()
    for task in data["items"]:
        assert task["status"] == "pending"


def test_get_tasks_invalid_status():
    # неверный статус – FastAPI вернёт 422
    response = requests.get(f"{BASE_URL}/tasks/?status=invalid_status")
    assert response.status_code == 422


def test_task_response_schema():
    create_resp = requests.post(
        f"{BASE_URL}/tasks/", json={"payload": {"check_schema": True}}
    )
    assert create_resp.status_code == 200
    task_id = create_resp.json()["task_id"]
    response = requests.get(f"{BASE_URL}/tasks/{task_id}")
    assert response.status_code == 200
    task = response.json()
    expected_keys = {
        "id",
        "status",
        "created_at",
        "updated_at",
        "result",
        "error_message",
    }
    # если payload возвращается, добавить его
    # expected_keys.add("payload")
    for key in expected_keys:
        assert key in task, f"Missing key: {key}"
    assert isinstance(task["id"], str)
    assert isinstance(task["status"], str)
    assert isinstance(task["created_at"], str)
    assert isinstance(task["updated_at"], str)
    assert task["result"] is None or isinstance(task["result"], dict)
    assert task["error_message"] is None or isinstance(task["error_message"], str)
