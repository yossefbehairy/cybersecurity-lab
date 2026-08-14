# Lab 02: Web Security

Difficulty: Beginner to Intermediate  
Estimated Time: 45-60 min  
OWASP: A03 - Injection (SQL Injection and XSS), A01 - Broken Access Control  
MITRE ATT&CK: T1190 - Exploit Public-Facing Application

## Learning Objectives

- Identify controlled SQL injection, XSS, and IDOR examples.
- Connect application behavior to generated security events.
- Propose secure remediation patterns.

## Scenario

The internal ordering portal is producing suspicious requests. Determine which routes are vulnerable and what evidence exists.

## Tasks

1. Test `/products`, `/comments`, and `/profile/<id>` locally.
2. Observe generated events in `/events`.
3. Explain impact and remediation for each weakness.

## Detection

Look for `web.sqli.pattern`, `web.xss.pattern`, and `web.idor.access` events.

## Remediation

Use parameterized SQL, contextual output encoding, and object-level authorization checks.

## Verification

You can map each finding to OWASP Top 10 and cite the related lab event.
