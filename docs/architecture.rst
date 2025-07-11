Architecture
------------
.. note::
   Please read the legal notice in the project `README.md` before using PiWardrive.


The diagram below illustrates the main components of PiWardrive and how they
interact.

.. graphviz::

   digraph architecture {
       rankdir=LR;
       node [shape=box, style=rounded];

       App [label="PiWardriveApp\n(piwardrive.main)"];
       Scheduler [label="PollScheduler\n(piwardrive.scheduler)"];
       Diagnostics [label="Diagnostics\n(piwardrive.diagnostics)"];
       Persistence [label="Persistence\n(piwardrive.persistence)"];
       Config [label="Config\n(piwardrive.config)"];
       Widgets [label="Widgets\n(widgets/)"];
       Screens [label="Screens\npiwardrive.screens"];
       Utils [label="Utils\n(piwardrive.utils)"];
       Logging [label="Logging\n(piwardrive.logconfig)"];
       External [label="External Services\n(Kismet, BetterCAP,\nGPSd, systemd)"];

       App -> Scheduler;
       App -> Diagnostics;
       App -> Config;
       App -> Persistence;
       App -> Screens;
       Screens -> Widgets;
       Widgets -> Scheduler;
       Widgets -> Utils;
       Diagnostics -> Persistence;
       Scheduler -> Diagnostics;
       Utils -> External;
       App -> Logging;
   App -> External [style=dashed, label="control"];
   }

Overview
~~~~~~~~

PiWardrive is composed of loosely coupled modules tied together by
``PiWardriveApp``. The **Scheduler** orchestrates polling of system metrics and
GPS data. **Diagnostics** gathers information about running services and writes
results to **Persistence** for later review. A browser-based dashboard provides
interactive maps and widgets that fetch data on a configurable interval using
the scheduler.

External services such as Kismet, BetterCAP and ``gpsd`` are controlled via
shell commands. They run outside the Python process but are monitored by the
application. Structured JSON logs are produced through
``piwardrive.logging.init_logging`` and written to ``~/.config/piwardrive/app.log`` by
default. The logger can also emit to ``stdout`` or extra handlers by calling
``logconfig.setup_logging`` for simple scripts.

Startup Sequence
~~~~~~~~~~~~~~~~

At startup ``piwardrive.main`` loads the configuration, initializes the scheduler and
restores any persisted ``AppState``. When the React frontend has been compiled,
``piwardrive.webui_server`` can serve it alongside the API so the same widgets
appear in a browser. Widgets register themselves with the scheduler to begin
polling. On shutdown the current state is saved so the next run resumes
exactly where the user left off.

