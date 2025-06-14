Architecture
------------

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

