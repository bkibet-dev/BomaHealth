import json
import os
import pytest

from cli.auth import register_flow, login_flow


@pytest.fixture(autouse=True)
def isolated_data_file(tmp_path, monkeypatch):
    """modules.auth.Auth reads/writes via modules.storage's data.json
    in the current working directory — isolate each test in its own dir."""
    monkeypatch.chdir(tmp_path)
    with open("data.json", "w") as f:
        json.dump({"supervisors": []}, f)
    yield


def test_register_flow_success(capsys):
    success = register_flow("Brandon Kibet", "brandon@test.com", "0712345678", "secret123", "secret123")

    assert success is True
    captured = capsys.readouterr()
    assert "registered successfully" in captured.out.lower()


def test_register_flow_fails_on_password_mismatch(capsys):
    success = register_flow("Brandon Kibet", "brandon2@test.com", "0712345678", "secret123", "different")

    assert success is False
    captured = capsys.readouterr()
    assert "do not match" in captured.out.lower()


def test_login_flow_success(capsys):
    register_flow("Brandon Kibet", "brandon3@test.com", "0712345678", "secret123", "secret123")
    capsys.readouterr()

    success = login_flow("brandon3@test.com", "secret123")

    assert success is True
    captured = capsys.readouterr()
    assert "welcome" in captured.out.lower()


def test_login_flow_fails_with_wrong_password(capsys):
    register_flow("Brandon Kibet", "brandon4@test.com", "0712345678", "secret123", "secret123")
    capsys.readouterr()

    success = login_flow("brandon4@test.com", "wrongpassword")

    assert success is False
    captured = capsys.readouterr()
    assert "wrong password" in captured.out.lower()