import logging
import time

from piwardrive.logging.filters import ContentFilter, RateLimiter, SensitiveDataFilter


def test_content_filter_include_exclude():
    config = {
        "include_patterns": ["error"],
        "exclude_patterns": ["ignore"],
    }
    cf = ContentFilter(config)

    record1 = logging.LogRecord(
        "test", logging.INFO, "", 0, "error occurred", None, None, None
    )
    record2 = logging.LogRecord(
        "test", logging.INFO, "", 0, "ignore this", None, None, None
    )

    assert cf.should_include(record1)
    assert not cf.should_include(record2)


def test_rate_limiter():
    rl = RateLimiter(max_rate=2, window_seconds=1)
    key = "test"
    assert rl.should_allow(key)
    assert rl.should_allow(key)
    assert not rl.should_allow(key)
    time.sleep(1.1)
    assert rl.should_allow(key)


def test_sensitive_data_redaction():
    sdf = SensitiveDataFilter({})
    text = "password=secret token=abcd email=test@example.com"
    redacted = sdf.redact_sensitive_data(text)
    assert "secret" not in redacted
    assert "abcd" not in redacted
    assert "test@example.com" not in redacted
