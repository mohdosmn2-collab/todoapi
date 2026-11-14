import pytest

import app as app_module


@pytest.fixture
def client():
    app_module.todos.clear()
    app_module.next_id = 1
    app_module.app.config["TESTING"] = True
    return app_module.app.test_client()


def test_health(client):
    assert client.get("/health").get_json() == {"status": "ok"}


def test_create_and_list(client):
    r = client.post("/todos", json={"title": "Learn Docker"})
    assert r.status_code == 201
    assert client.get("/todos").get_json()[0]["title"] == "Learn Docker"


def test_create_requires_title(client):
    assert client.post("/todos", json={}).status_code == 400


def test_update_and_delete(client):
    client.post("/todos", json={"title": "Task"})
    assert client.put("/todos/1", json={"done": True}).get_json()["done"] is True
    assert client.delete("/todos/1").status_code == 200
    assert client.delete("/todos/1").status_code == 404
