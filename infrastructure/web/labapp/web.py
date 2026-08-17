import os
import shutil
import threading
from pathlib import Path

from flask import Flask, jsonify, redirect, render_template, request, session, url_for

from .db import execute, initialize, query_all, query_one, wait_for_database
from .events import emit_event


app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "change-me-local-lab-secret")
UPLOAD_DIR = Path("/app/uploads")
_BOOTSTRAPPED = False
_BOOTSTRAP_LOCK = threading.Lock()


def bootstrap_once():
    """Initialise the database and uploads directory exactly once.

    Bug fix: the original implementation used a plain boolean flag with no
    locking, so concurrent first requests could race through the guard and
    call initialize() (which calls TRUNCATE + seed) multiple times.
    Using double-checked locking makes this safe under gunicorn with
    multiple threads.
    """
    global _BOOTSTRAPPED
    if _BOOTSTRAPPED:
        return
    with _BOOTSTRAP_LOCK:
        if not _BOOTSTRAPPED:   # double-checked locking
            initialize()
            UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
            _BOOTSTRAPPED = True


def clear_uploads():
    for path in UPLOAD_DIR.iterdir():
        if path.is_dir() and not path.is_symlink():
            shutil.rmtree(path)
        else:
            path.unlink()


@app.before_request
def before_request():
    bootstrap_once()


@app.get("/")
def index():
    return render_template("index.html", user=session.get("user"))


@app.get("/health")
def health():
    wait_for_database(timeout=5)
    return jsonify({"status": "ok", "service": "vulnerable-web", "lab": "local-training-only"})


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        user = query_one("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        if user:
            session["user"] = {"id": user["id"], "username": user["username"], "role": user["role"]}
            emit_event("auth.login.success", "info", "User logged in", username=username)
            return redirect(url_for("dashboard"))
        emit_event("auth.login.failure", "medium", "Failed login attempt", username=username, raw={"username": username})
        error = "Invalid username or password"
    return render_template("login.html", error=error)


@app.get("/logout")
def logout():
    username = session.get("user", {}).get("username")
    session.clear()
    emit_event("auth.logout", "info", "User logged out", username=username)
    return redirect(url_for("index"))


@app.get("/dashboard")
def dashboard():
    user_count = query_one("SELECT count(*) AS count FROM users")["count"]
    event_count = query_one("SELECT count(*) AS count FROM security_events")["count"]
    products = query_all("SELECT * FROM products ORDER BY id")
    return render_template("dashboard.html", user=session.get("user"), user_count=user_count, event_count=event_count, products=products)


@app.get("/products")
def products():
    q = request.args.get("q", "")
    db_error = None
    if q:
        emit_event("web.search", "info", "Product search submitted", raw={"q": q})
        if any(token in q.lower() for token in ["'", " union ", "--", " or "]):
            emit_event("web.sqli.pattern", "high", "SQL injection-like product search observed", raw={"q": q})
        sql = f"SELECT id, name, category, price FROM products WHERE lower(name) LIKE lower('%{q}%') ORDER BY id"
        try:
            rows = query_all(sql)
        except Exception as exc:
            emit_event("web.sqli.error", "high", "Database error after user-controlled product search", raw={"q": q, "error": str(exc)[:200]})
            rows = []
            db_error = "The database rejected this search. Treat this as investigation evidence in the local lab."
    else:
        rows = query_all("SELECT id, name, category, price FROM products ORDER BY id")
    return render_template("products.html", rows=rows, q=q, db_error=db_error)


@app.get("/profile/<int:user_id>")
def profile(user_id):
    viewer = session.get("user", {}).get("username")
    row = query_one("SELECT id, username, role, email, department, manager_id FROM users WHERE id = %s", (user_id,))
    if row and session.get("user", {}).get("id") != user_id:
        emit_event("web.idor.access", "medium", "User profile accessed without object ownership check", username=viewer, raw={"requested_user_id": user_id})
    return render_template("profile.html", profile=row, user=session.get("user"))


@app.route("/comments", methods=["GET", "POST"])
def comments():
    if request.method == "POST":
        author = request.form.get("author", "anonymous")[:40]
        body = request.form.get("body", "")
        # INTENTIONAL TRAINING BEHAVIOR — do not reorder for "security".
        # The INSERT happens before the pattern check so that students can:
        #   1. Submit an XSS payload,
        #   2. See it persist and render (via |safe in comments.html),
        #   3. Observe the delayed SIEM alert, and
        #   4. Understand why event-driven detection alone is insufficient.
        # The original code checked *after* insert — preserved intentionally.
        execute("INSERT INTO comments (author, body) VALUES (%s, %s)", (author, body))
        if "<script" in body.lower() or "onerror" in body.lower():
            emit_event("web.xss.pattern", "high", "Stored XSS-like comment submitted", username=author, raw={"body": body[:200]})
        return redirect(url_for("comments"))
    rows = query_all("SELECT * FROM comments ORDER BY id DESC")
    return render_template("comments.html", rows=rows)


@app.route("/upload", methods=["GET", "POST"])
def upload():
    message = None
    if request.method == "POST":
        uploaded = request.files.get("file")
        if uploaded and uploaded.filename:
            filename = Path(uploaded.filename).name
            destination = UPLOAD_DIR / filename
            uploaded.save(destination)
            emit_event("web.file.upload", "medium", "File uploaded without strong validation", raw={"filename": filename})
            message = f"Stored {filename} for local lab inspection"
    return render_template("upload.html", message=message)


@app.get("/admin/audit")
def audit():
    requested_role = request.args.get("role", "")
    if requested_role == "admin":
        emit_event("authz.role-bypass", "high", "Admin audit viewed through weak role check", username=session.get("user", {}).get("username"))
        rows = query_all("SELECT * FROM audit_records ORDER BY id DESC")
        return render_template("audit.html", rows=rows)
    return "Add ?role=admin to simulate a weak authorization check in this local-only lab.", 403


@app.post("/reset")
def reset():
    clear_uploads()
    initialize()
    return jsonify({"status": "reset", "deterministic": True})


if __name__ == "__main__":
    bootstrap_once()
    app.run(host="0.0.0.0", port=8080)
