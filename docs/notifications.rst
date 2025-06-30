Notifications
=============

PiWardrive can send HTTP POST requests to external services when certain
thresholds are exceeded.  CPU temperature and disk usage are monitored
by :class:`piwardrive.notifications.NotificationManager` which runs in the
background.

Configuration
-------------

Add webhook URLs to ``notification_webhooks`` inside ``config.json``.  The
``notify_cpu_temp`` and ``notify_disk_percent`` fields control when alerts are
triggered.  Example::

   {
       "notification_webhooks": ["http://localhost:9000/hook"],
       "notify_cpu_temp": 75.0,
       "notify_disk_percent": 85.0
   }

Webhooks receive a JSON body containing ``event`` and ``value`` keys.  Possible
events are ``"cpu_temp"`` and ``"disk_percent"``.

REST API
--------

The status service exposes ``/webhooks`` for managing the URL list::

   curl http://localhost:8000/webhooks
   curl -X POST -H 'Content-Type: application/json' \
        -d '["http://localhost:9000/hook"]' http://localhost:8000/webhooks

Testing
-------

Run a simple server that prints incoming requests::

   python -m http.server 9000

Then configure ``notification_webhooks`` to point at
``http://localhost:9000``.  Trigger high CPU load or fill the disk to verify
that a POST request is sent.
