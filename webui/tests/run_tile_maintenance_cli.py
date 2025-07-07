"""Test module for tile maintenance CLI functionality.

This module provides mock functions for tile maintenance operations and runs
the tile maintenance CLI for testing purposes.
"""
import json
import sys

from piwardrive.scripts import tile_maintenance_cli as cli

called = {}


def fake_purge(folder, days):
    """Mock function for tile purge operation.
    
    Args:
        folder: Folder path to purge tiles from.
        days: Number of days for purge threshold.
    """
    called["purge"] = [folder, int(days)]


def fake_limit(folder, limit):
    """Mock function for cache limit enforcement.
    
    Args:
        folder: Folder path to enforce limits on.
        limit: Cache size limit.
    """
    called["limit"] = [folder, int(limit)]


def fake_vacuum(path):
    """Mock function for database vacuum operation.
    
    Args:
        path: Path to database file to vacuum.
    """
    called["vacuum"] = path


cli.tile_maintenance.purge_old_tiles = fake_purge
cli.tile_maintenance.enforce_cache_limit = fake_limit
cli.tile_maintenance.vacuum_mbtiles = fake_vacuum

cli.main(sys.argv[1:])

print(json.dumps(called))
