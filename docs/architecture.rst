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

       App [label="PiWardriveApp\n(main.py)"];
       Scheduler [label="PollScheduler\n(scheduler.py)"];
       Diagnostics [label="Diagnostics\n(diagnostics.py)"];
       Persistence [label="Persistence\n(persistence.py)"];
       Config [label="Config\n(config.py)"];
       Widgets [label="Widgets\n(widgets/)"];
       Screens [label="Screens\nscreens/"];
       Utils [label="Utils\n(utils.py)"];
       Logging [label="Logging\n(logconfig.py)"];
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
results to **Persistence** for later review. **Screens** expose a touch-friendly
interface built with Kivy/KivyMD. Widgets run inside these screens and fetch
data on a configurable interval using the scheduler.

External services such as Kismet, BetterCAP and ``gpsd`` are controlled via
shell commands. They run outside the Python process but are monitored by the
application. Structured JSON logs are produced through
``logconfig.setup_logging`` and written to ``~/.config/piwardrive/app.log``.

Startup Sequence
~~~~~~~~~~~~~~~~

At startup ``main.py`` loads the configuration, initializes the scheduler and
restores any persisted ``AppState``. The GUI is then built from ``kv/main.kv``
and the initial screen is displayed. Widgets register themselves with the
scheduler to begin polling. On shutdown the current state is saved so the next
run resumes exactly where the user left off.

