import os
import pytest
from datetime import date, timedelta

from models import User, Task
from app import _build_postgres_uri


def test_is_overdue_future_date():
    task = Task(title="t", user_id=1, due_date=date.today() + timedelta(days=1))
    assert task.is_overdue() is False


def test_is_overdue_past_date():
    task = Task(title="t", user_id=1, due_date=date.today() - timedelta(days=1))
    assert task.is_overdue() is True


def test_password_hashing():
    user = User(username="bob")
    user.set_password("secret123")
    assert user.check_password("secret123") is True
    assert user.check_password("wrongpass") is False


def test_build_postgres_uri_env(monkeypatch):
    monkeypatch.setenv("POSTGRES_USER", "u")
    monkeypatch.setenv("POSTGRES_PASSWORD", "p")
    monkeypatch.setenv("POSTGRES_HOST", "h")
    monkeypatch.setenv("POSTGRES_PORT", "1111")
    monkeypatch.setenv("POSTGRES_DB", "mydb")

    uri = _build_postgres_uri()
    assert uri == "postgresql+psycopg2://u:p@h:1111/mydb"