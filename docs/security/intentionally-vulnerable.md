# Intentionally Vulnerable Behaviors — Cybersecurity Training Lab

> **WARNING**: Every weakness here is DELIBERATELY included for educational purposes.
> This application must NEVER be exposed to the public internet.

This document distinguishes **genuine engineering bugs** (fixed) from
**intentional training vulnerabilities** (preserved).

---

## 1. SQL Injection — `/products?q=`

| Field | Detail |
|-------|--------|
| **File** | `infrastructure/web/labapp/web.py` line 89 |
| **Code** | `sql = f"SELECT … LIKE lower('%{q}%') …"` |
| **Why it exists** | Students identify raw string interpolation in SQL |
| **Lab** | `labs/02-web-security`, `challenges/beginner/sql-injection` |
| **Impact** | Full read access to all tables |
| **How students discover it** | Test `'` and `' OR 1=1--` in the search box |
| **How defenders detect it** | `web.sqli.pattern` + `web.sqli.error` events in `/events` |
| **Correct remediation** | Parameterised queries: `query_all("… LIKE lower(%s)", (f"%{q}%",))` |
| **Must not be patched** | Primary SQLi training scenario |

---

## 2. Stored XSS — `/comments` + `comments.html`

| Field | Detail |
|-------|--------|
| **File** | `templates/comments.html` line 12 |
| **Code** | `{{ row.body|safe }}` — disables Jinja2 auto-escaping |
| **Why it exists** | Demonstrates escaped vs unescaped output |
| **Lab** | `labs/02-web-security`, `challenges/intermediate/stored-xss` |
| **Impact** | Arbitrary JS executes in every visitor's browser |
| **How students discover it** | Post `<script>alert(1)</script>` |
| **How defenders detect it** | `web.xss.pattern` event after insert |
| **Correct remediation** | Remove `|safe`; use `{{ row.body }}` |
| **Detection ordering note** | Alert fires AFTER insert intentionally — teaches that reactive alerting cannot prevent stored XSS |

---

## 3. IDOR — `/profile/<id>`

| Field | Detail |
|-------|--------|
| **File** | `web.py` lines 101-107 |
| **Why it exists** | Insecure Direct Object Reference — any ID accepted |
| **Lab** | `labs/02-web-security`, `challenges/intermediate/idor` |
| **Impact** | Any visitor can view any user profile |
| **How students discover it** | Increment path: `/profile/1`, `/profile/2` |
| **How defenders detect it** | `web.idor.access` event when viewer != target |
| **Correct remediation** | Compare session id with path id; return 403 if different |

---

## 4. Broken Access Control — `/admin/audit?role=admin`

| Field | Detail |
|-------|--------|
| **File** | `web.py` lines 137-144 |
| **Why it exists** | Client-supplied parameters cannot be trusted for authorisation |
| **Lab** | `labs/04-authentication`, `challenges/intermediate/broken-authz` |
| **Impact** | Any visitor reads all audit records via `?role=admin` |
| **How students discover it** | 403 body literally hints at the bypass |
| **How defenders detect it** | `authz.role-bypass` event |
| **Correct remediation** | Check `session["user"]["role"] == "admin"` |

---

## 5. Unrestricted File Upload — `/upload`

| Field | Detail |
|-------|--------|
| **File** | `web.py` lines 123-134 |
| **Why it exists** | Missing MIME-type and extension validation |
| **Lab** | `labs/02-web-security`, `challenges/advanced/file-upload` |
| **Impact** | Any file type (`.py`, `.sh`) stored on server |
| **How defenders detect it** | `web.file.upload` event; check file extensions |
| **Correct remediation** | Extension allowlist; set `MAX_CONTENT_LENGTH` |
| **Note** | `MAX_CONTENT_LENGTH` is absent deliberately for the exercise |

---

## 6. GET Logout — `/logout`

| Field | Detail |
|-------|--------|
| **File** | `web.py` line 65: `@app.get("/logout")` |
| **Why it exists** | Enables XSS chaining: `<img src="/logout">` in a comment logs out every visitor |
| **Lab** | `labs/02-web-security` — XSS chaining exercise |
| **How defenders detect it** | `auth.logout` events with no preceding login from same IP |
| **Correct remediation** | POST-only with CSRF token |

---

## 7. X-Forwarded-For Trust (Log Spoofing) — `events.py`

| Field | Detail |
|-------|--------|
| **File** | `events.py` line 13 |
| **Why it exists** | Teaches log-poisoning: forged `source_ip` in security events |
| **Lab** | `labs/06-soc-investigation` |
| **Impact** | Attacker inserts fake IP, misleads SOC analyst |
| **How students discover it** | Send requests with `X-Forwarded-For: 1.2.3.4` |
| **Correct remediation** | Trust only rightmost IP from a known proxy |

---

## 8. Plaintext Passwords

| Field | Detail |
|-------|--------|
| **File** | `db.py` lines 46-54, 119-124 |
| **Why it exists** | Students read credentials directly from DB |
| **Lab** | `labs/04-authentication` |
| **Correct remediation** | Hash with bcrypt/argon2 |

---

## Engineering Bugs Fixed (Not Training Vulnerabilities)

| Bug | File | Fix Applied |
|-----|------|-------------|
| `init_schema()` on every HTTP request | `logger.py` | One-time startup guard + `threading.Lock` |
| `?limit=abc` → HTTP 500 crash | `logger.py` | `try/except` → HTTP 400 |
| `bootstrap_once()` race condition | `web.py` | Double-checked locking with `threading.Lock` |
| Docker test ran in CI without Docker | `tests/test_static_project.py` | `pytest.mark.skipif` |
| `$env:POSTGRES_USER` unset crash | `scripts/health-check.ps1` | Fallback to `cyberlab` default |
