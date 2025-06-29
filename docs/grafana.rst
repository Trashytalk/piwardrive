Grafana Integration
-------------------

This guide explains how to visualize PiWardrive data in Grafana.

Export Data
~~~~~~~~~~~

Use the ``export-grafana`` command to generate a SQLite database with
``health_metrics`` and ``wifi_observations`` tables::

   export-grafana grafana.db --limit 5000

Grafana can connect to this database using the `SQLite data source
<https://grafana.com/grafana/plugins/fr-ser-sqlite-datasource/>`_.

Dashboards
~~~~~~~~~~

Two example dashboards live under ``grafana/dashboards``. Import the JSON
files through *Gear → Dashboards → Import*.

Quick Start
~~~~~~~~~~~

Start Grafana with Docker Compose::

   docker compose -f docker-compose.grafana.yml up

Login on <http://localhost:3000> (default ``admin/admin``), add the SQLite
data source pointing at ``grafana.db`` and import the dashboards.
