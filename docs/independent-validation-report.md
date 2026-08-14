# Independent Student Validation Report

Validation date: 2026-08-14  
Scope: local Docker training environment only

## Challenge Results

| Challenge | Difficulty | Attempted Successfully | Student Instructions | Hints | Solution | Logging | Reset | OWASP Mapping | MITRE Mapping | Issues Found | Issues Fixed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Linux Baseline Review | Beginner | YES | PASS | PASS | PASS | PASS (not required by objective) | PASS | N/A | PASS: T1082 | None | None |
| Network Service Map | Beginner | YES | PASS | PASS | PASS | PASS (health checks intentionally do not create event noise) | PASS | N/A | PASS: T1595 | Detection text incorrectly implied a health/recon event | Corrected the lab guidance |
| Stored XSS Triage | Beginner | YES | PASS | PASS | PASS | PASS | PASS | PASS: A03 - Injection | PASS: N/A, browser-side vulnerability | None | Removed the forced JavaScript ATT&CK mapping |
| Broken Authorization Investigation | Intermediate | YES | PASS | PASS | PASS | PASS | PASS | PASS: A01 - Broken Access Control | PASS: N/A, access-control weakness | None | Removed the forced Valid Accounts ATT&CK mapping |
| Suspicious Login Investigation | Intermediate | YES | PASS after correction | PASS after correction | PASS | PASS | PASS | PASS: A07 - Identification and Authentication Failures | PASS: T1110 | No student-visible valid credentials | Published deterministic fake local-only accounts |
| SQL Injection Investigation | Intermediate | YES | PASS after correction | PASS | PASS | PASS | PASS | PASS: A03 - Injection | PASS: T1190 | Normal product search failed before a meaningful comparison was possible | Fixed unparameterized-query execution so normal and injection paths both work |
| Multi-Stage Incident Investigation | Advanced | YES | PASS after correction | PASS | PASS | PASS | PASS | PASS: A01 and A03 | PASS: T1190 | Successful-login credentials were not visible to students | Uses the published deterministic fake account |
| Forensic Timeline Reconstruction | Advanced | YES | PASS | PASS | PASS | PASS (static evidence exercise) | PASS | N/A | PASS: N/A, defensive evidence analysis | A Windows event implied privileged logon rather than the documented role bypass | Removed the contradictory synthetic event |

## Technical Validation

- All services start healthy through the documented PowerShell workflow.
- `web` and `logging` are bound only to `127.0.0.1`; PostgreSQL has no host port.
- `lab_net` and `backend_net` are internal. `analyst-tools` can resolve and reach `web:8080`, cannot resolve the database, and has no external route.
- Custom services run non-root with read-only root filesystems, dropped capabilities, and `no-new-privileges`.
- SQL injection, stored XSS rendering, IDOR, weak authorization, unrestricted file type handling, and weak session flags were exercised only against the local lab.
- Structured events were confirmed for successful and failed login, suspicious search, application error, upload, IDOR, and authorization bypass.
- Reset restores the deterministic database/event baseline and now removes uploaded files.

## Automated Validation

- `docker compose config --quiet`: PASS
- `py -m pytest -q tests/test_static_project.py`: PASS (5 tests)
- `RUN_DOCKER_TESTS=1 py -m pytest -q tests/test_live_lab.py`: PASS (4 tests)
- `powershell -ExecutionPolicy Bypass -File scripts/final-audit.ps1`: PASS

## Final Verdict

PORTFOLIO READY

## Remaining Limitations

- The intentional weaknesses must remain local-only and must never be deployed publicly.
- Windows evidence is synthetic; the project does not include Windows virtual machines or live endpoint telemetry.
- On Windows installations without GNU Make or a POSIX shell, students should use the documented PowerShell equivalents.
