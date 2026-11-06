"""Desktop host. The browser UI and analysis API share a loopback origin."""

import argparse
import ctypes
import json
import logging
import os
import sys
import threading
from logging.handlers import RotatingFileHandler
from pathlib import Path
from urllib.request import urlopen

from flask import abort, send_from_directory
from smoke import check_analysis
from waitress import create_server

from app import create_app

logger = logging.getLogger(__name__)


def frontend_directory():
    if getattr(sys, "frozen", False):
        return Path(__file__).resolve().parent / "frontend"
    return Path(__file__).resolve().parents[1] / "app/front-end/dist"


def create_desktop_app(frontend):
    frontend = Path(frontend).resolve()
    if not (frontend / "index.html").is_file():
        raise FileNotFoundError("Frontend build missing. Run the desktop build script first.")
    app = create_app()

    @app.get("/")
    def index():
        return send_from_directory(frontend, "index.html")

    @app.get("/<path:filename>")
    def assets(filename):
        # Missing API paths must remain 404, never return the SPA document.
        if filename == "api" or filename.startswith("api/"):
            abort(404)
        return send_from_directory(frontend, filename)

    return app


def data_directory():
    base = Path(os.environ.get("LOCALAPPDATA", Path.home() / ".local/share"))
    directory = base / "ChronoGeoLab"
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke-test", action="store_true", help="Check bundled UI/API without a GUI")
    args = parser.parse_args()
    directory = data_directory()
    handler = RotatingFileHandler(directory / "desktop.log", maxBytes=2_000_000, backupCount=2)
    logging.basicConfig(level=logging.INFO, handlers=[handler])
    os.environ.setdefault("STP_OSM_CACHE_DIR", str(directory / "osm-cache"))
    server = None
    thread = None
    try:
        app = create_desktop_app(frontend_directory())
        # Bind port 0 directly: the OS chooses a free port without a reservation race.
        server = create_server(app, host="127.0.0.1", port=0, threads=4)
        thread = threading.Thread(target=server.run, daemon=True)
        thread.start()
        url = f"http://127.0.0.1:{server.effective_port}"
        with urlopen(f"{url}/api/v1/health", timeout=15) as response:
            assert json.load(response)["status"] == "healthy"
        if args.smoke_test:
            with urlopen(url, timeout=15) as response:
                assert b"<html" in response.read().lower()
            with urlopen(f"{url}/api/v1/tools", timeout=15) as response:
                assert response.status == 200
            check_analysis(url)
            print("Desktop smoke test passed: bundled UI and all four analysis tools available.")
        else:
            import webview

            webview.create_window("ChronoGeoLab", url, width=1440, height=960, min_size=(1000, 700))
            webview.start(
                gui="edgechromium" if sys.platform == "win32" else None,
                storage_path=str(directory / "webview"),
            )
        return 0
    except Exception:
        logger.exception("Desktop startup failed")
        if sys.platform == "win32" and not args.smoke_test:
            ctypes.windll.user32.MessageBoxW(
                0,
                f"ChronoGeoLab could not start. Ensure Microsoft Edge WebView2 Runtime is installed.\n"
                f"Details: {directory / 'desktop.log'}",
                "ChronoGeoLab",
                0x10,
            )
        return 1
    finally:
        if server is not None:
            server.task_dispatcher.shutdown()
            server.close()
        if thread is not None:
            thread.join(timeout=3)


if __name__ == "__main__":
    raise SystemExit(main())
