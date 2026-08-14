# Lab 03: Linux Security

Difficulty: Beginner  
Estimated Time: 30-45 min  
MITRE ATT&CK: T1082 - System Information Discovery

## Learning Objectives

- Inspect a constrained Linux container safely.
- Understand non-root execution, dropped capabilities, and read-only filesystems.
- Verify tool boundaries for the analyst environment.

## Scenario

The analyst environment should support learning without becoming an unrestricted attack box.

## Tasks

1. Enter `analyst-tools`.
2. Confirm the current user is not root.
3. Inspect writable paths and installed tools.
4. Explain why this environment has no host-published ports.

## Detection

Linux inspection commands are local to the lab container and should not target external hosts.

## Remediation

Harden containers with non-root users, minimal packages, dropped capabilities, and `no-new-privileges`.

## Verification

You can describe at least three container hardening controls in this lab.

