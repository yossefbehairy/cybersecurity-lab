# Lab 04: Authentication And Authorization

Difficulty: Intermediate  
Estimated Time: 45-60 min  
OWASP: A01 - Broken Access Control, A07 - Identification and Authentication Failures  
MITRE ATT&CK: T1078 - Valid Accounts

## Learning Objectives

- Investigate failed and successful login events.
- Identify weak authorization decisions.
- Separate authentication from authorization.

## Scenario

Several failed logins are followed by privileged activity. Determine whether the activity is expected.

## Tasks

1. Attempt login with the fake account `alice` and password `Password123!`.
2. Review failed login events.
3. Investigate `/admin/audit`.
4. Explain why query-string role checks are unsafe.

## Detection

Look for `auth.login.failure`, `auth.login.success`, and `authz.role-bypass`.

## Remediation

Use server-side role checks, strong session management, rate limiting, and audit logging.

## Verification

You can identify which event indicates authorization bypass behavior.
