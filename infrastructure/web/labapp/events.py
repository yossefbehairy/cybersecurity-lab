import os

import requests
from flask import request


LOGGING_URL = os.getenv("LOGGING_URL", "http://logging:8082/events")


def emit_event(event_type, severity, message, username=None, raw=None):
    payload = {
        "source_service": "vulnerable-web",
        "source_ip": request.headers.get("X-Forwarded-For", request.remote_addr) if request else None,
        "username": username,
        "event_type": event_type,
        "severity": severity,
        "endpoint": request.path if request else None,
        "method": request.method if request else None,
        "message": message,
        "raw": raw or {},
    }
    try:
        requests.post(LOGGING_URL, json=payload, timeout=2)
    except requests.RequestException:
        pass

