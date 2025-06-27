Function Flows
==============
.. note::
   Please read the legal notice in the project `README.md` before using PiWardrive.


The diagrams below illustrate how key functions operate inside
PiWardrive. These complement the high level overview in
:doc:`architecture`.

PollScheduler.register_widget
-----------------------------

.. mermaid::

   sequenceDiagram
       participant Widget
       participant Scheduler
       participant Clock

       Widget->>Scheduler: register_widget()
       Scheduler->>Widget: check update_interval
       Scheduler->>Clock: schedule_interval(widget.update, interval)
       Clock-->>Scheduler: event handle

utils.run_async_task
--------------------

.. mermaid::

   sequenceDiagram
       participant Caller
       participant run_async_task
       participant asyncio

       Caller->>run_async_task: coroutine + callback
       run_async_task->>asyncio: run_coroutine_threadsafe()
       asyncio-->>run_async_task: Future
       run_async_task->>Future: add_done_callback()
       run_async_task-->>Caller: return Future

Scheduled SIGINT scans
----------------------

Like ``PollScheduler.register_widget`` above, scheduled tasks invoke the
SIGINT suite scanners and persist their results.

.. mermaid::

   sequenceDiagram
       participant Scheduler
       participant Scanners
       participant Persistence

       Scheduler->>Scanners: scan_wifi(), scan_bluetooth(), ...
       Scanners-->>Scheduler: results
       Scheduler->>Persistence: save results

