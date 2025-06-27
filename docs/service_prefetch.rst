Service Prefetching
===================
.. note::
   Please read the legal notice in the project `README.md` before using PiWardrive.

This guide demonstrates how to prefetch common API endpoints so the data is ready when the dashboard loads.  The asynchronous approach fetches multiple routes in parallel and can run periodically in the background.

Example Script
--------------

Install ``httpx`` if it is not already available::

   pip install httpx

Use :mod:`asyncio` and ``httpx.AsyncClient`` to gather responses concurrently::

   import asyncio
   import httpx

   ENDPOINTS = [
       "/status",
       "/widget-metrics",
       "/cpu",
       "/ram",
       "/storage",
   ]

   async def prefetch(base_url: str) -> dict:
       async with httpx.AsyncClient() as client:
           tasks = [client.get(base_url.rstrip("/") + ep) for ep in ENDPOINTS]
           responses = await asyncio.gather(*tasks)
           return {ep: r.json() for ep, r in zip(ENDPOINTS, responses)}

   if __name__ == "__main__":
       data = asyncio.run(prefetch("http://localhost:8000"))
       print(data)

The ``prefetch`` coroutine returns a dictionary mapping each endpoint to its parsed JSON response.  This can be saved to disk or stored in memory for quick access.

Scheduling Prefetches
---------------------

``PollScheduler`` from :mod:`piwardrive.scheduler` can invoke ``prefetch`` on a timer.  Register the task when your application starts::

   from piwardrive.scheduler import PollScheduler
   scheduler = PollScheduler()
   scheduler.schedule(
       "service_prefetch",
       lambda _dt: asyncio.create_task(prefetch("http://localhost:8000")),
       interval=60,
   )

The example above refreshes the cached data once per minute.  Adjust the interval based on how frequently clients require updated information.
