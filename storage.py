"""Storage: holds submissions and the audit log.

NOTE: this is in-memory (a list and a dict), same as the original single-file
version. That means both are wiped on every process restart -- including
Flask's debug-mode auto-reloader, which restarts on every code change. If you
want your audit log / submissions to survive restarts (recommended before you
capture final evidence for your README), swap this module's internals for
SQLite without changing its function signatures, and nothing in app.py needs
to change.
"""
from datetime import datetime, timezone

audit_log = []
submissions = {}


def create_audit_entry(entry):
    entry["timestamp"] = datetime.now(timezone.utc).isoformat()
    audit_log.append(entry)


def get_log():
    return audit_log


def save_submission(content_id, submission):
    submissions[content_id] = submission


def get_submission(content_id):
    return submissions.get(content_id)