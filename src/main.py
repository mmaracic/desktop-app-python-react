"""Desktop application entry point combining FastAPI, uvicorn, and pywebview."""

import uvicorn
import webview
from fastapi import FastAPI
from src.api import root

APP_HOST = "127.0.0.1"
APP_PORT = 5000
APP_URL = f"http://{APP_HOST}:{APP_PORT}"

app = FastAPI()
app.include_router(root.router)


def _run_backend_server() -> None:
    """Start the uvicorn server in a background thread."""
    config = uvicorn.Config(app, host=APP_HOST, port=APP_PORT, log_level="info")
    server = uvicorn.Server(config)
    server.run()


def main() -> None:
    """Launch the desktop window with the embedded FastAPI server."""

    webview.create_window("Hello world", APP_URL)
    webview.start(_run_backend_server)


if __name__ == "__main__":
    main()
