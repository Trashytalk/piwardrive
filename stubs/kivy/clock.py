"""Minimal stubs emulating :mod:`kivy.clock` for tests."""


class DummyEvent:
    """Placeholder for scheduled events."""
    def cancel(self):
        """No-op used by tests."""
        pass


class Clock:
    """Simplified clock implementation used in headless tests."""
    @staticmethod
    def schedule_interval(callback, interval):
        """Return a dummy event for periodic callbacks."""
        return DummyEvent()

    @staticmethod
    def schedule_once(callback, timeout=0):
        """Return a dummy event for a one-shot callback."""
        return DummyEvent()

    @staticmethod
    def create_trigger(callback, timeout=0, interval=True):
        """Return a callable that proxies to ``callback``."""
        def trigger(*args, **kwargs):
            return callback(*args, **kwargs)
        return trigger

    @staticmethod
    def unschedule(ev):
        """Ignore unscheduling requests."""
        pass


def mainthread(func):
    """Decorator returning ``func`` unchanged for tests."""
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
