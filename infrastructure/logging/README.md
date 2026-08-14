# Logging Service

The logging service reuses the Python application image and runs `python -m labapp.logger`.

It stores structured events in PostgreSQL and exposes a localhost-bound API on port `8082` for training investigations.

