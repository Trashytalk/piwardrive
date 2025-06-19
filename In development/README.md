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
   ```

   The compiled assets will be placed in `webui/dist`.

2. Launch the API with the static build:

   ```bash
   python 'In development/browser_server.py'
   ```

   The server listens on `http://0.0.0.0:8000` and serves the API under `/api` as well as the built React interface.

## MapLibre Prototype

This lightweight framework mirrors the Kivy dashboard using plain HTML, Tailwind and MapLibre. Static files live in `web_gui/` and the FastAPI backend is defined in `piwardrive.web_api`.
The `/api/widgets` endpoint exposes the available dashboard widgets from `piwardrive.widgets` so the frontend can render them dynamically.

Start it with:

```bash
uvicorn piwardrive.web_api:app --host 0.0.0.0 --port 5000
```

Open `http://localhost:5000` in Chromium (kiosk mode is supported). The API provides endpoints for GPS, AP and BT data as well as starting or stopping Kismet.
