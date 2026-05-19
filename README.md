# Readme

Python desktop application with React Typescript UI using PyWebView.  
https://pywebview.flowrl.com/


## Setup
Run the following command to install the dependencies:
```bash
uv sync
```
## Run
Run the application with:
```bash
uv run -m src.main
```
Application has parameters for host, port and no-frontend. You can run the application without frontend with:
```bash
uv run -m src.main --no-frontend
```

## Features
- FastAPI backend server
- separate API router for backend endpoints
- React frontend served from the FastAPI backend as static files using `StaticFiles` middleware and mounting the React build directory
- React Typescript frontend built with Vite
- PyWebView creates a frontend window and serves the React app from the FastAPI backend
- Backend server runs in a background thread, allowing the application to exit gracefully when the webview window is closed
- Logging for backend server startup and webview window events
- Command-line arguments for configuring host, port, and whether to run without the frontend

# Issues
- It would be better if backend would be able to serve the React app without needing to build it first. Currently, you need to run `npm run build` in the React project to generate the static files that the FastAPI backend serves.