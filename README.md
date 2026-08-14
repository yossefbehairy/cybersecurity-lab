# Cybersecurity Training Lab

A lightweight, portfolio-ready cybersecurity training platform that simulates a small enterprise environment for local red-team and blue-team practice.

> Security warning: this repository contains intentionally vulnerable services for local training only. Do not expose it to the internet, do not point tools at external systems, and do not use real credentials or personal data.

## What You Learn

- Network reconnaissance inside an isolated Docker network
- Web application security using controlled OWASP Top 10 examples
- Linux security basics from a constrained analyst environment
- Authentication and authorization weaknesses
- SOC-style log review and event triage
- Incident response and digital forensics with synthetic evidence
- Remediation thinking, not command memorization

## Architecture

```text
                         localhost only
                   +-----------------------+
                   | Web App :8080         |
                   | Logging API :8082     |
                   +----------+------------+
                              |
             +----------------+----------------+
             |                                 |
        lab_net internal                 backend_net internal
             |                                 |
   +---------+----------+          +-----------+----------+
   | analyst-tools      |          | PostgreSQL database  |
   | constrained tools  |          | no host port exposed |
   +--------------------+          +-----------+----------+
                                               |
                                    +----------+----------+
                                    | lightweight logging |
                                    | events in Postgres  |
                                    +---------------------+
```

`lab_net` and `backend_net` are marked `internal: true`. A narrow `access_net` exists only so the host can reach `127.0.0.1:8080` and `127.0.0.1:8082`. The database is never exposed to the host. The `analyst-tools` container has no published ports and only joins the lab network.

## Requirements

- Docker Desktop with Docker Compose
- Git
- 4 CPU threads recommended
- 8 GB RAM minimum, 16 GB recommended
- Ports `8080` and `8082` available on localhost

## Quick Start

```bash
git clone <your-fork-url>
cd cybersecurity-lab
cp .env.example .env
make setup
```

If `make` is not available:

```bash
sh scripts/setup.sh
```

On Windows PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/setup.ps1
```

Access:

- Web app: <http://localhost:8080>
- Logging API: <http://localhost:8082/events?limit=20>
- Analyst shell: `docker compose exec analyst-tools sh`

## Training Accounts

All accounts and passwords are deterministic, fake, and limited to this local lab. Use them only against `localhost:8080`.

| Username | Role | Password |
| --- | --- | --- |
| `alice` | analyst | `Password123!` |
| `bob` | employee | `Password123!` |
| `carol` | admin | `Password123!` |
| `dave` | employee | `Password123!` |

## Core Commands

```bash
make setup    # build, start, and verify the lab
make start    # start services
make status   # show service state
make health   # verify app, database, logging, and containers
make reset    # reset deterministic seed data and logs
make stop     # stop services
make test     # run static tests
```

Windows PowerShell equivalents:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/setup.ps1
powershell -ExecutionPolicy Bypass -File scripts/start.ps1
powershell -ExecutionPolicy Bypass -File scripts/stop.ps1
docker compose ps
powershell -ExecutionPolicy Bypass -File scripts/health-check.ps1
powershell -ExecutionPolicy Bypass -File scripts/reset.ps1
py -m pytest -q
```

Final local audit:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/final-audit.ps1
```

## Training Progression

1. Beginner: Linux basics, network reconnaissance, basic web vulnerability discovery.
2. Intermediate: authentication issues, web exploitation evidence, log analysis.
3. Advanced: multi-source incident response and forensic timeline reconstruction.

Each challenge includes difficulty, estimated time, OWASP mapping where relevant, MITRE ATT&CK mapping, skills, hints, and a separated solution guide.

## Technologies

- Docker Compose
- Python Flask
- PostgreSQL
- Lightweight structured logging API
- Pytest
- GitHub Actions

## GitHub Topics

`cybersecurity`, `cybersecurity-lab`, `penetration-testing`, `soc`, `blue-team`, `red-team`, `docker`, `network-security`, `web-security`, `digital-forensics`, `cybersecurity-training`

## Known Limitations

- v1 intentionally avoids Elastic, Kibana, and Wazuh to stay usable on a 16 GB laptop.
- Windows security is represented through synthetic Windows-style logs and forensic exercises, not a Windows VM.
- The dashboard is intentionally minimal so the project remains training-first.

## Roadmap

- Optional Loki/Promtail profile for larger machines.
- More secure-code remediation branches.
- Additional MITRE technique coverage.
- Exportable incident report templates.
