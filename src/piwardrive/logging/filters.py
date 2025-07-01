import logging
import re
import time
from collections import defaultdict, deque
from typing import Any, Dict, List, Optional, Pattern


class ContentFilter:
    """Filters logs based on content patterns."""

    def __init__(self, config: Dict[str, Any]):
        self.include_patterns: List[Pattern] = []
        self.exclude_patterns: List[Pattern] = []
        self.keyword_filters: Dict[str, List[str]] = {}
        self._load_patterns(config)

    def _load_patterns(self, config: Dict[str, Any]):
        """Load regex patterns from configuration."""
        for pattern in config.get("include_patterns", []):
            self.include_patterns.append(re.compile(pattern))

        for pattern in config.get("exclude_patterns", []):
            self.exclude_patterns.append(re.compile(pattern))

    def should_include(self, record: logging.LogRecord) -> bool:
        """Check if record should be included based on content."""
        message = record.getMessage()

        # Check exclude patterns first (more efficient)
        for pattern in self.exclude_patterns:
            if pattern.search(message):
                return False

        # If include patterns are defined, message must match at least one
        if self.include_patterns:
            return any(pattern.search(message) for pattern in self.include_patterns)

        return True


class RateLimiter:
    """Rate limiting for log messages."""

    def __init__(self, max_rate: int, window_seconds: int):
        self.max_rate = max_rate
        self.window_seconds = window_seconds
        self.message_counts: Dict[str, deque] = defaultdict(deque)

    def should_allow(self, message_key: str) -> bool:
        """Check if message should be allowed based on rate limits."""
        now = time.time()
        cutoff = now - self.window_seconds

        # Clean old entries
        while (
            self.message_counts[message_key]
            and self.message_counts[message_key][0] < cutoff
        ):
            self.message_counts[message_key].popleft()

        # Check rate limit
        if len(self.message_counts[message_key]) >= self.max_rate:
            return False

        # Record this message
        self.message_counts[message_key].append(now)
        return True


class SensitiveDataFilter:
    """Filters and redacts sensitive information from logs."""

    def __init__(self, config: Dict[str, Any]):
        self.patterns = {}
        self.redaction_rules = {}
        self._load_patterns(config)

    def _load_patterns(self, config: Dict[str, Any]):
        """Load sensitive data patterns."""
        patterns = {
            "password": r'password["\']?\s*[:=]\s*["\']?([^"\'\s]+)',
            "api_key": r'api[_-]?key["\']?\s*[:=]\s*["\']?([^"\'\s]+)',
            "token": r'token["\']?\s*[:=]\s*["\']?([^"\'\s]+)',
            "ssn": r"\b\d{3}-\d{2}-\d{4}\b",
            "credit_card": r"\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b",
            "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
        }

        for name, pattern in patterns.items():
            self.patterns[name] = re.compile(pattern, re.IGNORECASE)

    def redact_sensitive_data(self, text: str) -> str:
        """Redact sensitive data from text."""
        redacted = text

        for name, pattern in self.patterns.items():
            redacted = pattern.sub(f"[REDACTED_{name.upper()}]", redacted)

        return redacted
