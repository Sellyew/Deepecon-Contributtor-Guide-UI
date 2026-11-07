"""Keep invitation tokens out of logs (plan §2.2 and §3)."""
import logging
import re

TOKEN_PATH = re.compile(r"/i/[^/\s\"'?]+")


def redact(text):
    return TOKEN_PATH.sub("/i/[redacted]", text) if isinstance(text, str) else text


class RedactInvitationTokens(logging.Filter):
    """Rewrites any /i/<token> path in a log record's message and arguments."""

    def filter(self, record):
        record.msg = redact(record.msg)
        if isinstance(record.args, tuple):
            record.args = tuple(redact(a) for a in record.args)
        elif isinstance(record.args, dict):
            record.args = {k: redact(v) for k, v in record.args.items()}
        # django.request attaches the request; its path must not be formatted later.
        if hasattr(record, "request"):
            record.request = None
        return True
