API Usage Examples
===================

The following examples demonstrate typical requests against the PiWardrive API.

Authentication
--------------
Obtain a token using the OAuth2 password flow::

    curl -X POST "http://localhost:8000/token" \
        -H "Content-Type: application/x-www-form-urlencoded" \
        -d "username=admin&password=secret"

Use the returned token when calling other endpoints::

    curl -H "Authorization: Bearer <token>" http://localhost:8000/status

Exporting Access Points
-----------------------
Retrieve cached access point data as GeoJSON::

    curl -H "Authorization: Bearer <token>" \
         http://localhost:8000/export/aps?fmt=geojson -o aps.geojson
