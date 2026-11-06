"""Verify the desktop HTTP boundary independently of the windowing runtime."""

import importlib.util
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parents[1]))
spec = importlib.util.spec_from_file_location("desktop_main", Path(__file__).parents[1] / "main.py")
desktop = importlib.util.module_from_spec(spec)
spec.loader.exec_module(desktop)


def test_desktop_serves_ui_assets_and_real_api(tmp_path):
    (tmp_path / "index.html").write_text("<html>desktop</html>")
    (tmp_path / "assets").mkdir()
    (tmp_path / "assets/main.js").write_text("console.log('desktop')")
    client = desktop.create_desktop_app(tmp_path).test_client()
    assert client.get("/").data == b"<html>desktop</html>"
    assert client.get("/assets/main.js").status_code == 200
    assert client.get("/api/v1/health").json["status"] == "healthy"
    assert client.get("/api/v1/tools").status_code == 200
    for path in ("/api/unknown", "/assets/missing.js", "/../main.py", "/assets/../../main.py"):
        assert client.get(path).status_code == 404


def test_missing_frontend_fails_before_opening_window(tmp_path):
    with pytest.raises(FileNotFoundError, match="Frontend build missing"):
        desktop.create_desktop_app(tmp_path)
