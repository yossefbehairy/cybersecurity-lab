import os
import subprocess

import pytest
import requests


pytestmark = pytest.mark.skipif(
    os.getenv("RUN_DOCKER_TESTS") != "1",
    reason="set RUN_DOCKER_TESTS=1 after starting Docker to run live container tests",
)


def test_web_and_logging_are_reachable():
    assert requests.get("http://localhost:8080/health", timeout=5).json()["status"] == "ok"
    assert requests.get("http://localhost:8082/health", timeout=5).json()["status"] == "ok"


def test_logging_event_creation_and_reset():
    response = requests.get("http://localhost:8080/products?q=%27%20or%201%3D1--", timeout=5)
    assert response.status_code == 200
    events = requests.get("http://localhost:8082/events?type=web.sqli.pattern&limit=5", timeout=5).json()
    assert events["count"] >= 1
    reset = requests.post("http://localhost:8080/reset", timeout=5)
    assert reset.json()["deterministic"] is True


def test_reset_removes_uploaded_files_and_restores_event_baseline():
    upload = requests.post(
        "http://localhost:8080/upload",
        files={"file": ("validation.txt", b"synthetic training evidence", "text/plain")},
        timeout=5,
    )
    assert upload.status_code == 200
    before_reset = subprocess.run(
        ["docker", "compose", "exec", "-T", "web", "sh", "-lc", "test -f /app/uploads/validation.txt"],
        text=True,
        capture_output=True,
        timeout=20,
    )
    assert before_reset.returncode == 0

    reset = requests.post("http://localhost:8080/reset", timeout=5)
    assert reset.json()["deterministic"] is True
    after_reset = subprocess.run(
        ["docker", "compose", "exec", "-T", "web", "sh", "-lc", "test ! -e /app/uploads/validation.txt"],
        text=True,
        capture_output=True,
        timeout=20,
    )
    assert after_reset.returncode == 0
    events = requests.get("http://localhost:8082/events?limit=5", timeout=5).json()
    assert events["count"] == 1
    assert events["events"][0]["event_type"] == "lab.reset"


def test_analyst_container_has_no_published_ports():
    result = subprocess.run(
        ["docker", "compose", "port", "analyst-tools", "80"],
        text=True,
        capture_output=True,
        timeout=20,
    )
    assert result.stdout.strip() == ""
