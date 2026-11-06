"""Run with: uv run --project desktop python desktop/build.py"""

import argparse
import os
import platform
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-install", action="store_true", help="Reuse frontend node_modules")
    args = parser.parse_args()
    desktop = Path(__file__).resolve().parent
    root = desktop.parent
    npm = shutil.which("npm.cmd" if sys.platform == "win32" else "npm")
    if npm is None:
        raise SystemExit("Install Node.js 24 (including npm) before building.")
    frontend = root / "app/front-end"
    if not args.skip_install:
        subprocess.run([npm, "ci"], cwd=frontend, check=True)
    env = dict(os.environ, VITE_BACKEND_URL="")
    subprocess.run([npm, "run", "build"], cwd=frontend, env=env, check=True)
    subprocess.run(
        [sys.executable, "-m", "PyInstaller", "--noconfirm", "--clean",
         "--distpath", str(desktop / "dist"), "--workpath", str(desktop / "build"),
         str(desktop / "ChronoGeoLab.spec")],
        cwd=desktop, check=True,
    )
    output = desktop / "dist/ChronoGeoLab"
    executable = output / ("ChronoGeoLab.exe" if sys.platform == "win32" else "ChronoGeoLab")
    with tempfile.TemporaryDirectory(prefix="chronogeolab-smoke-") as test_directory:
        test_env = dict(os.environ, LOCALAPPDATA=test_directory)
        try:
            subprocess.run(
                [str(executable), "--smoke-test"], env=test_env, check=True, timeout=90,
            )
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
            log = Path(test_directory) / "ChronoGeoLab/desktop.log"
            if log.is_file():
                print(log.read_text(errors="replace"), file=sys.stderr)
            raise
    archive = shutil.make_archive(
        str(desktop / f"dist/ChronoGeoLab-{sys.platform}-{platform.machine()}"),
        "zip", root_dir=output.parent, base_dir=output.name,
    )
    print(f"Desktop bundle ready: {archive}")


if __name__ == "__main__":
    main()
