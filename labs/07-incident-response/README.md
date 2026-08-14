# Lab 07: Incident Response

Difficulty: Advanced  
Estimated Time: 75-90 min  
OWASP: A01 - Broken Access Control  
MITRE ATT&CK: T1078 - Valid Accounts, T1190 - Exploit Public-Facing Application

## Learning Objectives

- Build a timeline from multiple event types.
- Identify initial access and follow-on activity.
- Recommend containment and recovery.

## Scenario

An admin audit page was viewed after suspicious authentication activity.

## Tasks

1. Generate failed login and role-bypass events.
2. Review the security event stream.
3. Determine what happened first.
4. Write containment, eradication, and recovery steps.

## Detection

Correlate `auth.login.failure`, `auth.login.success`, and `authz.role-bypass`.

## Remediation

Apply server-side authorization, alerting, credential review, and access log retention.

## Verification

You can produce a timeline and a short incident response plan.

