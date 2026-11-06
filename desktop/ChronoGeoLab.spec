from pathlib import Path

from PyInstaller.utils.hooks import collect_all

desktop = Path(SPECPATH)
root = desktop.parent
datas = [(str(root / "app/front-end/dist"), "frontend"), (str(root / "LICENSE"), ".")]
binaries = []
hiddenimports = []
# These packages load native libraries/data or select implementations dynamically.
# NumPy, SciPy, Shapely and webview are handled by the standard/contrib hooks.
for package in ("pyproj", "pyogrio", "h3"):
    package_datas, package_binaries, package_imports = collect_all(package)
    datas += package_datas
    binaries += package_binaries
    hiddenimports += package_imports

a = Analysis(
    [str(desktop / "main.py")],
    pathex=[str(root / "app/back-end")],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    excludes=["pytest", "tkinter", "IPython"],
)
pyz = PYZ(a.pure)
exe = EXE(
    pyz, a.scripts, [], exclude_binaries=True,
    name="ChronoGeoLab", console=False,
)
coll = COLLECT(exe, a.binaries, a.datas, name="ChronoGeoLab")
