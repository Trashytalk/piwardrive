# Browser-based Setup (Experimental)

This directory contains prototypes for running PiWardrive in a self-hosted browser environment in place of the Kivy GUI.

Two approaches are provided:

1. **React Prototype** (`webui/`)
2. **MapLibre Prototype** (`web_gui/`)

## React Prototype

This uses a small React application built with Vite.

1. Build the frontend:

   ```bash
   cd webui
   npm install
   npm run build
    cd ..
   ```

   The compiled assets will be placed in `webui/dist`.

   During development you can run `npm run dev` which starts a Vite server
   that proxies API calls to `http://localhost:8000`.

2. Launch the API with the static build from the repository root:

   ```bash
   python -m piwardrive.webui_server
   ```

   The server listens on `http://0.0.0.0:8000` and serves the API under `/api` as well as the built React interface.

## MapLibre Prototype

This lightweight framework mirrors the Kivy dashboard using plain HTML, Tailwind and MapLibre. Static files live in `web_gui/` and the FastAPI backend is defined in `web_api.py`.

Start it with:

```bash
uvicorn web_api:app --host 0.0.0.0 --port 5000
```

Open `http://localhost:5000` in Chromium (kiosk mode is supported). The API provides endpoints for GPS, AP and BT data as well as starting or stopping Kismet.

### Serving Offline Tiles

MapLibre can display vector or raster tiles from a local `mbtiles` database. One easy way to host the file is with [`mbtileserver`](https://github.com/consbio/mbtileserver).

Run the container and mount your tiles directory:

```bash
docker run --rm -p 8080:8000 -v /mnt/ssd/tiles:/tilesets ghcr.io/consbio/mbtileserver:latest
```

The MBTiles file `offline.mbtiles` will then be available at `http://localhost:8080/services/offline`. `web_gui/app.js` is configured to point the map at this endpoint.
