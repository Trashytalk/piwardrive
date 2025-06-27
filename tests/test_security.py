import os

import pytest

from piwardrive import security


def test_hash_and_verify_password() -> None:
    h = security.hash_password("secret")
    assert security.verify_password("secret", h)
    assert not security.verify_password("wrong", h)


def test_validate_service_name() -> None:
    security.validate_service_name("good.service")
    with pytest.raises(ValueError):
        security.validate_service_name("../bad")


def test_sanitize_path_valid() -> None:
    path = os.path.join("a", "b", "..", "c.txt")
    assert security.sanitize_path(path) == os.path.normpath(path)


@pytest.mark.parametrize("path", ["../etc/passwd", "a/../../secret.txt"])
def test_sanitize_path_invalid(path: str) -> None:
    with pytest.raises(ValueError):
        security.sanitize_path(path)
