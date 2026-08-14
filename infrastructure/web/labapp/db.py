import os
import sys
import time
from contextlib import contextmanager

import psycopg
from psycopg.rows import dict_row
from psycopg.types.json import Jsonb


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://cyberlab:change-me-local-only@database:5432/cyberlab",
)


@contextmanager
def connect():
    conn = psycopg.connect(DATABASE_URL, row_factory=dict_row)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def wait_for_database(timeout=60):
    start = time.time()
    while time.time() - start < timeout:
        try:
            with connect() as conn:
                conn.execute("SELECT 1")
                return
        except Exception:
            time.sleep(1)
    raise RuntimeError("database did not become ready")


def init_schema():
    with connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL,
                email TEXT NOT NULL,
                department TEXT NOT NULL,
                manager_id INTEGER
            );
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                price NUMERIC(10,2) NOT NULL
            );
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY,
                user_id INTEGER NOT NULL REFERENCES users(id),
                product_id INTEGER NOT NULL REFERENCES products(id),
                quantity INTEGER NOT NULL,
                status TEXT NOT NULL
            );
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS comments (
                id SERIAL PRIMARY KEY,
                author TEXT NOT NULL,
                body TEXT NOT NULL,
                created_at TIMESTAMPTZ DEFAULT now()
            );
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS audit_records (
                id SERIAL PRIMARY KEY,
                actor TEXT NOT NULL,
                action TEXT NOT NULL,
                target TEXT NOT NULL,
                created_at TIMESTAMPTZ DEFAULT now()
            );
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS security_events (
                id SERIAL PRIMARY KEY,
                event_time TIMESTAMPTZ DEFAULT now(),
                source_service TEXT NOT NULL,
                source_ip TEXT,
                username TEXT,
                event_type TEXT NOT NULL,
                severity TEXT NOT NULL,
                endpoint TEXT,
                method TEXT,
                message TEXT NOT NULL,
                raw JSONB DEFAULT '{}'::jsonb
            );
            """
        )


def seed_data():
    users = [
        (1, "alice", "Password123!", "analyst", "alice@example.test", "Security", None),
        (2, "bob", "Password123!", "employee", "bob@example.test", "Sales", 1),
        (3, "carol", "Password123!", "admin", "carol@example.test", "IT", 1),
        (4, "dave", "Password123!", "employee", "dave@example.test", "Finance", 3),
    ]
    products = [
        (1, "Acme VPN Gateway", "network", 1299.00),
        (2, "Endpoint Sensor", "security", 89.00),
        (3, "Cloud Backup Seat", "storage", 12.50),
        (4, "Privileged Access Token", "internal", 0.01),
    ]
    orders = [
        (1, 1, 2, 5, "approved"),
        (2, 2, 3, 12, "pending"),
        (3, 3, 1, 1, "approved"),
        (4, 4, 4, 2, "review"),
    ]
    audit_records = [
        ("system", "seed", "baseline-data", "2026-01-15T09:00:00Z"),
        ("carol", "role-review", "alice", "2026-01-15T09:00:30Z"),
        ("alice", "ticket-opened", "suspicious-login-case-001", "2026-01-15T09:01:00Z"),
    ]

    with connect() as conn:
        conn.execute("TRUNCATE security_events, comments, audit_records, orders, products, users RESTART IDENTITY CASCADE")
        with conn.cursor() as cur:
            cur.executemany(
                "INSERT INTO users (id, username, password, role, email, department, manager_id) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                users,
            )
            cur.executemany(
                "INSERT INTO products (id, name, category, price) VALUES (%s,%s,%s,%s)",
                products,
            )
            cur.executemany(
                "INSERT INTO orders (id, user_id, product_id, quantity, status) VALUES (%s,%s,%s,%s,%s)",
                orders,
            )
            cur.executemany(
                "INSERT INTO audit_records (actor, action, target, created_at) VALUES (%s,%s,%s,%s)",
                audit_records,
            )
        conn.execute(
            """
            INSERT INTO security_events
              (event_time, source_service, source_ip, username, event_type, severity, endpoint, method, message, raw)
            VALUES
              ('2026-01-15T09:00:00Z', 'seed', '127.0.0.1', 'system', 'lab.reset', 'info', '/reset', 'SYSTEM', 'Deterministic lab baseline loaded', %s)
            """,
            (Jsonb({"case": "baseline"}),),
        )


def initialize():
    wait_for_database()
    init_schema()
    seed_data()


def query_one(sql, params=None):
    with connect() as conn:
        if params is None:
            return conn.execute(sql).fetchone()
        return conn.execute(sql, params).fetchone()


def query_all(sql, params=None):
    with connect() as conn:
        if params is None:
            return conn.execute(sql).fetchall()
        return conn.execute(sql, params).fetchall()


def execute(sql, params=None):
    with connect() as conn:
        if params is None:
            conn.execute(sql)
        else:
            conn.execute(sql, params)


if __name__ == "__main__":
    command = sys.argv[1] if len(sys.argv) > 1 else "initialize"
    if command in {"initialize", "reset"}:
        initialize()
        print("database initialized with deterministic seed data")
    elif command == "schema":
        wait_for_database()
        init_schema()
        print("database schema ready")
    else:
        raise SystemExit(f"unknown command: {command}")
