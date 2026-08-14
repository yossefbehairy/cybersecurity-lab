# Scenario

An audit page may be accessible through a weak authorization check.

## Objective

Determine whether access is controlled by trusted server-side state or user-controlled input.

## Tasks

1. Visit `/admin/audit`.
2. Observe the denied response.
3. Review what input changes the outcome.
4. Find the related logging event.
5. Explain a secure authorization design.

