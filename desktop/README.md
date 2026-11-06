# Windows 桌面试用包

使用 pywebview + Waitress + PyInstaller，复用现有 React 界面和 Flask 分析 API。
本地服务仅监听 `127.0.0.1`，由系统分配空闲端口；界面和 API 使用同一个地址。
退出窗口后关闭服务。网页/Docker 启动方式不受影响。

## 在 Windows 构建 exe

构建机需要 Windows x64、Python 3.12、Node.js 24 和 uv。
从仓库根目录（包含 `package.json` 和 `desktop` 的目录）运行：

```powershell
uv sync --project desktop --locked --python 3.12
uv run --project desktop --locked pytest desktop/tests -v
uv run --project desktop --locked python desktop/build.py
```

脚本安装前端依赖、构建界面、生成 PyInstaller 文件夹包，并运行打包后的无窗口自检。
前端构建时强制使用本地同源 API，覆盖开发环境中的 `VITE_BACKEND_URL`。
已有 `node_modules` 时可加 `--skip-install`。

生成文件：

- `desktop/dist/ChronoGeoLab/ChronoGeoLab.exe`
- `desktop/dist/ChronoGeoLab-win32-AMD64.zip`（架构名称取决于构建机）

分享整个 zip，接收方解压后双击 exe。**必须保留同目录中的 `_internal` 文件夹**；
这是便携试用包，还不是安装程序或单文件 exe。
接收方无需安装 Python、Node.js 或 Docker，但必须具备
[Microsoft Edge WebView2 Runtime](https://developer.microsoft.com/en-us/microsoft-edge/webview2/)。
Windows 版强制使用 Edge Chromium，避免回退到不能渲染现代 3D 地图的旧引擎。

也可推送代码后，在 GitHub Actions 手动运行 **Windows desktop bundle** 工作流，
完成后下载 `ChronoGeoLab-Windows-x64` 构建产物。工作流不自动发布 Release。

## 本地开发与验证

构建前端后，可直接运行桌面入口或无窗口自检：

```powershell
uv run --project desktop --locked python desktop/main.py
uv run --project desktop --locked python desktop/main.py --smoke-test
```

Linux 也可运行构建脚本验证打包，但产物是 Linux 可执行文件，无法生成 Windows exe。
Linux 上显示窗口还需安装 pywebview 支持的 GTK/WebKit 或 Qt 图形环境；无窗口自检不需要它们。
桌面依赖使用独立虚拟环境和 `desktop/uv.lock`，不修改后端运行环境。

日志位于 Windows 的 `%LOCALAPPDATA%/ChronoGeoLab/desktop.log`，
道路缓存和 WebView 数据也保存在该用户目录。Linux 对应 `~/.local/share/ChronoGeoLab/`。
启动失败时先看日志；Windows 窗口模式还会显示错误提示。

## 首次交付检查

打包脚本自检覆盖真实可执行文件中的静态首页、健康检查、工具列表和四类工具的离线示例计算，
不能替代 Windows 图形环境验收。首次交付应在没有 Python/Node/Docker 的 Windows 机器上检查：

- 打开地图、旋转缩放 3D 视图。
- 上传 CSV/GeoJSON，运行轨迹、棱柱、STKDE、时空立方体并导出结果。
- 关闭窗口后可以重新打开；日志中没有缺失 DLL、PROJ 或 GDAL 数据错误。
- 中文路径和文件名可用；缺少 WebView2 时提示可理解。

底图和在线道路查询仍需联网。完整离线地图、安装向导、代码签名和自动升级尚未包含。
