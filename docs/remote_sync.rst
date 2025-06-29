Remote Data Sync
================

.. note::
   Please read the legal notice in the project `README.md` before using PiWardrive.

This guide explains how to backhaul PiWardrive's health data to a server over WireGuard.  It covers configuration on the Pi as well as a minimal FastAPI receiver that can run on your router or another host.

Prerequisites
-------------

* Pi running PiWardrive and a GL.iNet router with WireGuard configured.
* A host reachable over the VPN to collect uploads.
* Python 3.10+ installed on the remote host.

Server Setup
------------

1. Create a small FastAPI application on the remote host that accepts POST uploads.  ``remote_sync.sync_database_to_server`` sends the SQLite database using ``multipart/form-data``.  The example below saves each upload under ``~/piwardrive-sync``::

    from fastapi import FastAPI, UploadFile
    import os, shutil

    app = FastAPI()
    STORAGE = os.path.expanduser('~/piwardrive-sync')
    os.makedirs(STORAGE, exist_ok=True)

    @app.post('/')
    async def receive(file: UploadFile):
        dest = os.path.join(STORAGE, file.filename)
        with open(dest, 'wb') as fh:
            shutil.copyfileobj(file.file, fh)
        return {'saved': dest}

    if __name__ == '__main__':
        import uvicorn
        uvicorn.run(app, host='0.0.0.0', port=9000)

   Run the server with ``python sync_receiver.py`` or using systemd.  Ensure port
   ``9000`` is reachable via the WireGuard tunnel.

Client Configuration
--------------------

1. Edit ``~/.config/piwardrive/config.json`` and set ``remote_sync_url`` to the
   receiver's URL, for example ``"http://10.0.0.2:9000/"``.  Optionally define
   ``remote_sync_token`` if your server expects a bearer token.
2. ``remote_sync_timeout`` and ``remote_sync_retries`` control how long PiWardrive
   waits for a response and how many times it retries on failure.
   ``remote_sync_interval`` schedules automatic uploads when greater than
   ``0`` and represents the frequency in minutes.  See
   ``examples/remote_sync.json`` for a snippet with common values.
3. Restart PiWardrive or reload the configuration to apply the changes.

Uploading Data
--------------

Use the ``/sync`` endpoint exposed by ``piwardrive.service`` or call
``remote_sync.sync_database_to_server`` directly::

    curl -X POST http://localhost:8000/sync

    # or in Python
    import asyncio, remote_sync
    asyncio.run(remote_sync.sync_database_to_server(
        '~/.config/piwardrive/health.db',
        'http://10.0.0.2:9000/'
    ))

The database will be uploaded to the server where it can be processed or backed
up as needed.

Python API
----------

``remote_sync.sync_database_to_server`` is an asynchronous helper that takes the
path to a SQLite database and an upload URL.  Optional ``timeout`` and
``retries`` parameters control how long the call waits for a response and how
many attempts are made before giving up.  The function raises
``aiohttp.ClientError`` on network failures.

Example::

    import asyncio
    from piwardrive import remote_sync

    asyncio.run(
        remote_sync.sync_database_to_server(
            "~/piwardrive/health.db",
            "http://10.0.0.2:9000/",
            timeout=10,
            retries=5,
        )
    )

Command Line Helper
-------------------

PiWardrive also provides ``scripts/serviceSync.js`` for headless systems. The
Node script can upload the database and check service status in one command.
It accepts the following options:

``--db``
    Path to the SQLite database to upload.
``--url``
    Destination URL that receives the file via HTTP ``POST``.
``--services``
    One or more systemd service names to query with ``systemctl``.

Example invocation::

    node scripts/serviceSync.js \
        --db ~/.config/piwardrive/health.db \
        --url http://10.0.0.2:9000/ \
        --services piwardrive piwardrive-webui

Collecting Metrics
------------------

Set the environment variable ``PW_REMOTE_SYNC_METRICS=1`` or call
``remote_sync.enable_metrics()`` to track upload statistics. When
enabled, ``remote_sync.get_metrics()`` returns ``success_total`` and
``failure_total`` counters along with the duration of the last sync.

