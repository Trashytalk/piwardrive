import json
import sys

from piwardrive.scripts import tile_maintenance_cli as cli

called = {}


def fake_purge(folder, days):
    called["purge"] = [folder, int(days)]


def fake_limit(folder, limit):
    called["limit"] = [folder, int(limit)]


def fake_vacuum(path):
    called["vacuum"] = path


cli.tile_maintenance.purge_old_tiles = fake_purge
cli.tile_maintenance.enforce_cache_limit = fake_limit
cli.tile_maintenance.vacuum_mbtiles = fake_vacuum

cli.main(sys.argv[1:])

print(json.dumps(called))
