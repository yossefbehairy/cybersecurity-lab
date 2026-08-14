# Contributing

Contributions should keep the lab safe, deterministic, and local-only.

## Rules

- Do not add external targets or internet attack automation.
- Do not add real credentials, real personal data, or copied breach data.
- Keep challenges reproducible after `make reset`.
- Keep student instructions separate from solution guides.
- Add OWASP and MITRE ATT&CK mappings when relevant.
- Prefer lightweight services over memory-heavy stacks unless they are optional profiles.

## Development

```bash
cp .env.example .env
docker compose config --quiet
python -m pytest -q
```

For live tests:

```bash
make setup
RUN_DOCKER_TESTS=1 python -m pytest -q tests/test_live_lab.py
```

