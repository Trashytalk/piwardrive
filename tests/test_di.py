import os
import sys
from unittest import mock
import threading
import pytest

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


def test_concurrent_resolve_creates_single_instance() -> None:
    c = Container()

    created: list[object] = []

    def factory() -> object:
        obj = object()
        created.append(obj)
        return obj

    c.register_factory("svc", factory)

    results: list[object] = []

    def worker() -> None:
        results.append(c.resolve("svc"))

    threads = [threading.Thread(target=worker) for _ in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert len(created) == 1
    assert all(r is results[0] for r in results)
