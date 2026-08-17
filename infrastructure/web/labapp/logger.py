import threading

from flask import Flask, jsonify, request
from psycopg.types.json import Jsonb

from .db import connect, init_schema, wait_for_database


app = Flask(__name__)

# One-time startup guard — prevents calling init_schema() on every request.
# Bug fix: the original @before_request hook ran CREATE TABLE IF NOT EXISTS
# six times per HTTP call, adding unnecessary round-trips to every response.
_SCHEMA_READY = False
_SCHEMA_LOCK = threading.Lock()


def ensure_schema_once():
    """Initialise the DB schema exactly once, thread-safely."""
    global _SCHEMA_READY
    if _SCHEMA_READY:
        return
    with _SCHEMA_LOCK:
        if not _SCHEMA_READY:   # double-checked locking
            init_schema()
            _SCHEMA_READY = True


@app.before_request
def ensure_schema():
    ensure_schema_once()


@app.get("/health")
def health():
    wait_for_database(timeout=5)
    return jsonify({"status": "ok", "service": "logging"})


@app.post("/events")
def create_event():
    data = request.get_json(force=True, silent=True) or {}
    with connect() as conn:
        row = conn.execute(
            """
            INSERT INTO security_events
              (source_service, source_ip, username, event_type, severity, endpoint, method, message, raw)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
            RETURNING id
            """,
            (
                data.get("source_service", "unknown"),
                data.get("source_ip"),
                data.get("username"),
                data.get("event_type", "unknown"),
                data.get("severity", "info"),
                data.get("endpoint"),
                data.get("method"),
                data.get("message", "event recorded"),
                Jsonb(data.get("raw", {})),
            ),
        ).fetchone()
    return jsonify({"id": row["id"], "status": "recorded"}), 201


@app.get("/events")
def list_events():
    severity = request.args.get("severity")
    event_type = request.args.get("type")
    # Bug fix: int() on an arbitrary query-string value raised ValueError (HTTP 500).
    # Now invalid values return a clear 400 response instead of crashing.
    raw_limit = request.args.get("limit", "50")
    try:
        limit = max(1, min(int(raw_limit), 200))
    except (ValueError, TypeError):
        return jsonify({"error": "'limit' must be a positive integer (1–200)"}), 400
    where = []
    params = []
    if severity:
        where.append("severity = %s")
        params.append(severity)
    if event_type:
        where.append("event_type = %s")
        params.append(event_type)
    sql = "SELECT * FROM security_events"
    if where:
        sql += " WHERE " + " AND ".join(where)
    sql += " ORDER BY id DESC LIMIT %s"
    params.append(limit)
    with connect() as conn:
        events = conn.execute(sql, params).fetchall()
    return jsonify({"events": events, "count": len(events)})


if __name__ == "__main__":
    wait_for_database()
    init_schema()
    app.run(host="0.0.0.0", port=8082)
