"""Desktop application entry point combining FastAPI, uvicorn, and pywebview."""

import argparse
from fastapi.staticfiles import StaticFiles
import logging
from pydantic import BaseModel
import uvicorn
from src.colored_log_formatter import ColoredLogFormatter
import threading
import webview
from fastapi import FastAPI
from src.api import api

log_handler = logging.StreamHandler()
log_handler.setFormatter(
    ColoredLogFormatter(
        fmt="%(asctime)s %(levelname)s %(threadName)s %(name)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
)
logging.basicConfig(level=logging.INFO, handlers=[log_handler])
logger = logging.getLogger(__name__)


class Config(BaseModel):
    """Configuration for the application."""

    host: str = "127.0.0.1"
    port: int = 5000
    no_frontend: bool = False


app = FastAPI()
app.include_router(api.router)
app.mount("/", StaticFiles(directory="react/dist", html=True))


def _run_backend_server(config: Config) -> None:
    """Start the uvicorn server in a background thread."""
    uvicorn_config = uvicorn.Config(
        app, host=config.host, port=config.port, log_level="info", log_config=None
    )
    server = uvicorn.Server(uvicorn_config)
    server.run()


def parse_args() -> Config:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Agentic desktop application")
    parser.add_argument(
        "--host", type=str, default="127.0.0.1", help="Host for the backend server"
    )
    parser.add_argument(
        "--port", type=int, default=5000, help="Port for the backend server"
    )
    parser.add_argument(
        "--no-frontend",
        type=bool,
        default=False,
        help="Disable the frontend window, default is False",
    )
    args = parser.parse_args()
    return Config(host=args.host, port=args.port, no_frontend=args.no_frontend)


def main() -> None:
    """Main entry point for the application."""
    config = parse_args()

    if config.no_frontend:
        _run_backend_server(config)
        return

    # Python application shuts down when only daemon threads are running.
    # Running the backend server in a daemon thread rather than in webview start method
    # allows the application to exit gracefully when the webview window is closed.
    thread = threading.Thread(target=_run_backend_server, args=(config,), daemon=True)
    thread.start()

    server = f"http://{config.host}:{config.port}"
    logger.info("Backend server starting at %s", server)
    window = webview.create_window("Hello world", server)
    if window is None:
        logger.error("Failed to create webview window, shutting down backend server...")
        return
    window.events.shown += lambda: logger.info("Webview window is now visible")
    webview.start()
    logger.info("Webview window closed, shutting down backend server...")


if __name__ == "__main__":
    main()
