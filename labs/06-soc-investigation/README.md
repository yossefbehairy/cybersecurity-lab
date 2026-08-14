# Lab 06: SOC Investigation

Difficulty: Intermediate  
Estimated Time: 60-75 min  
OWASP: A03 - Injection  
MITRE ATT&CK: T1190 - Exploit Public-Facing Application

## Learning Objectives

- Triage suspicious web events.
- Separate benign errors from high-confidence attack patterns.
- Document indicators of compromise.

## Scenario

Acme Supply reports suspicious database query behavior from the product search page.

## Tasks

1. Generate normal and suspicious product searches.
2. Query high severity events.
3. Identify request patterns and timestamps.
4. Write a short incident note with impact and containment.

## Detection

Look for `web.sqli.pattern` and compare it to ordinary `web.search` events.

## Remediation

Prioritize parameterized queries and centralized detection for injection markers.

## Verification

Your incident note includes initial signal, affected endpoint, impact, and remediation.

