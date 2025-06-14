import pytest
import security


def test_hash_and_verify_password() -> None:
    h = security.hash_password("secret")
    assert security.verify_password("secret", h)
    assert not security.verify_password("wrong", h)


def test_validate_service_name() -> None:
    security.validate_service_name("good.service")
    with pytest.raises(ValueError):
        security.validate_service_name("../bad")
