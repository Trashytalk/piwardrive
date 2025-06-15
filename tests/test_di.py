import os
import sys
from unittest import mock
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from piwardrive.di import Container


def test_register_instance_and_resolve() -> None:
    c = Container()
    obj = object()
    c.register_instance("svc", obj)
    assert c.has("svc") is True
    assert c.resolve("svc") is obj


def test_register_factory_and_single_instance() -> None:
    c = Container()
    factory = mock.Mock(return_value=object())
    c.register_factory("svc", factory)
    assert c.has("svc") is True
    first = c.resolve("svc")
    second = c.resolve("svc")
    assert first is second
    factory.assert_called_once()


def test_resolve_missing_key_raises() -> None:
    c = Container()
    with pytest.raises(KeyError):
        c.resolve("missing")
