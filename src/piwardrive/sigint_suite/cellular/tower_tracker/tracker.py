"""Compatibility wrapper importing the actual tracker implementation."""

# The real implementation lives under ``piwardrive.integrations.sigint_suite``.
# This thin module allows older import paths used in some tests to keep working.
try:  # pragma: no cover - optional implementation
    from piwardrive.integrations.sigint_suite.cellular.tower_tracker.tracker import *  # type: ignore  # noqa: F401, F403, E501
except Exception:
    # Minimal stub used when optional integrations are unavailable
    class TowerTracker:
        def __init__(self, _path: str) -> None:
            self.path = _path

        async def update_tower(self, *_a, **_k) -> None:
            pass

        async def get_tower(self, *_a, **_k):
            return None

        async def all_towers(self):
            return []

        async def log_wifi(self, *_a, **_k) -> None:
            pass

        async def log_bluetooth(self, *_a, **_k) -> None:
            pass

        async def wifi_history(self, *_a, **_k):
            return []

        async def bluetooth_history(self, *_a, **_k):
            return []

        async def log_tower(self, *_a, **_k) -> None:
            pass

        async def tower_history(self, *_a, **_k):
            return []

        async def close(self) -> None:
            pass
