# Browser-based Setup (Experimental)

This directory contains an experimental setup for running PiWardrive in a self-hosted browser environment instead of the Kivy GUI.

The browser UI uses the existing React project under `webui/` and the FastAPI service found in `piwardrive.service`.

## Quick start

1. Build the frontend using Node and Vite:

   ```bash
   cd webui
   npm install
   npm run build
   ```

   The compiled assets will be placed in `webui/dist`.

2. Start the API server with static file hosting:

   ```bash
   python 'In development/browser_server.py'
   ```

   The server listens on `http://0.0.0.0:8000` and serves the API under `/api` as well as the built web interface at the root path.

This mode is optional and not integrated with the main Kivy application.  It is a work in progress and may change frequently.
