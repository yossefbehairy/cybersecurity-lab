# Solution Guide

The vulnerable route builds SQL with string interpolation:

```python
sql = f"SELECT ... WHERE lower(name) LIKE lower('%{q}%')"
```

Expected evidence:

- suspicious input submitted to `/products`
- abnormal product results or database error behavior
- `web.sqli.pattern` event with endpoint and raw query

Fix: use parameterized queries and avoid constructing SQL from request strings.

