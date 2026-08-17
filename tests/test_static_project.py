from pathlib import Path
import re
import shutil
import subprocess

import pytest


ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


def test_compose_declares_isolated_networks_and_no_database_port():
    compose = read("docker-compose.yml")
    assert "access_net:" in compose
    assert "lab_net:" in compose
    assert "backend_net:" in compose
    assert "internal: true" in compose
    database_block = compose.split("  logging:", 1)[0]
    assert "ports:" not in database_block


def test_security_baseline_present_for_custom_services():
    compose = read("docker-compose.yml")
    for service in ["web", "logging", "analyst-tools"]:
        pattern = rf"  {service}:\n(?P<body>.*?)(?:\n  [a-zA-Z0-9_-]+:|\nnetworks:)"
        body = re.search(pattern, compose, flags=re.S).group("body")
        assert "read_only: true" in body
        assert "cap_drop:" in body
        assert "no-new-privileges:true" in body


def test_challenge_metadata_contains_mitre_and_owasp_for_web_challenges():
    challenge_readmes = list((ROOT / "challenges").glob("*/*/README.md"))
    assert len(challenge_readmes) >= 8
    for path in challenge_readmes:
        text = path.read_text(encoding="utf-8")
        assert "Difficulty:" in text
        assert "Estimated Time:" in text
        assert "MITRE ATT&CK:" in text
        if "web" in text.lower() or "SQL Injection" in text or "XSS" in text:
            assert "OWASP:" in text


def test_no_elastic_kibana_wazuh_in_v1_compose():
    compose = read("docker-compose.yml").lower()
    assert "kibana" not in compose
    assert "elastic" not in compose
    assert "wazuh" not in compose
    assert "5601" not in compose


@pytest.mark.skipif(
    shutil.which("docker") is None,
    reason="Docker binary not found; skipping live compose-config validation",
)
def test_docker_compose_config_when_docker_available():
    """Validate docker-compose.yml is syntactically valid.

    Bug fix: previously this test ran unconditionally and failed in any
    environment where the Docker daemon was absent (e.g. static-only CI),
    making the entire test suite report failures unrelated to the code
    under test.  Now it is skipped when docker is not on PATH.
    """
    result = subprocess.run(
        ["docker", "compose", "config", "--quiet"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        timeout=60,
    )
    assert result.returncode == 0, result.stderr
