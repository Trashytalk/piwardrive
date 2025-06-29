GPSD Clients
------------
.. note::
   Please read the legal notice in the project `README.md` before using PiWardrive.

`gpsd_client` and `gpsd_client_async` provide simple wrappers around
`gpsd <https://gpsd.gitlab.io/gpsd/>`_. Both modules expose a default
client instance and helpers to query latitude, longitude and fix details.

Synchronous Usage
~~~~~~~~~~~~~~~~~

The :class:`piwardrive.gpsd_client.GPSDClient` maintains a thread-safe
connection. ``client`` is a pre-initialised instance used throughout the
application::

   from piwardrive.gpsd_client import client
   lat_lon = client.get_position()
   accuracy = client.get_accuracy()
   fix = client.get_fix_quality()

The client reconnects automatically when ``gpsd`` becomes available.

Asynchronous Usage
~~~~~~~~~~~~~~~~~~

For asyncio applications :mod:`gpsd_client_async` offers the
:class:`piwardrive.gpsd_client_async.AsyncGPSDClient`. The ``async_client``
singleton behaves like its synchronous counterpart but methods return
``await``-able coroutines::

   from piwardrive.gpsd_client_async import async_client

   async def poll():
       pos = await async_client.get_position_async()
       acc = await async_client.get_accuracy_async()
       fix = await async_client.get_fix_quality_async()

Both clients support explicit ``host`` and ``port`` arguments. By default they
read ``PW_GPSD_HOST`` and ``PW_GPSD_PORT`` from the environment, falling back to
``127.0.0.1`` and ``2947``.
