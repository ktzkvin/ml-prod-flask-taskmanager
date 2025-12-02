import pytest
from app import create_app
from extensions import db
from models import User, Task


@pytest.fixture
def test_app():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["WTF_CSRF_ENABLED"] = False

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(test_app):
    return test_app.test_client()


def test_register_and_login(client):
    # Register
    r = client.post("/register", data={
        "username": "john",
        "password": "secret",
        "confirm": "secret"
    }, follow_redirects=True)
    assert r.status_code == 200

    # Login
    r = client.post("/login", data={
        "username": "john",
        "password": "secret"
    }, follow_redirects=True)
    assert b"Logged in successfully" in r.data


def test_create_task(client):
    # Register + login
    client.post("/register", data={
        "username": "bob",
        "password": "pass",
        "confirm": "pass"
    })
    client.post("/login", data={"username": "bob", "password": "pass"})

    # Create task
    r = client.post("/tasks/new", data={
        "title": "task1",
        "description": "desc",
        "due_date": ""
    }, follow_redirects=True)

    assert r.status_code == 200
    assert b"Task created" in r.data


def test_toggle_task(client):
    # Register + login
    client.post("/register", data={
        "username": "anna",
        "password": "pass",
        "confirm": "pass"
    })
    client.post("/login", data={"username": "anna", "password": "pass"})

    # Create a task
    client.post("/tasks/new", data={"title": "t", "description": "", "due_date": ""})
    # Toggle task id 1
    r = client.post("/tasks/1/toggle", follow_redirects=True)

    assert r.status_code == 200
    assert b"Task status updated" in r.data