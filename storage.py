"""Storage: holds submissions and the audit log.
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
