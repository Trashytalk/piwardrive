"""Compatibility wrapper importing the actual tracker implementation."""

# The real implementation lives under ``piwardrive.integrations.sigint_suite``.
# This thin module allows older import paths used in some tests to keep working.
from piwardrive.integrations.sigint_suite.cellular.tower_tracker.tracker import *  # noqa: F401,F403,E501
