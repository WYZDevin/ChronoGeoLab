# 快速上手

[English](./getting-started.md) | 简体中文

本指南将带你从一台全新的电脑开始，完成第一次时空分析。最简单的方式是使用
**Docker Desktop**，它会为你运行前端和后端——无需安装 Python、Node.js
或任何 GIS 软件。

## 第 1 步——安装 Docker Desktop

1. 从 <https://www.docker.com/products/docker-desktop/> 下载
   **Docker Desktop**（Windows、Mac 或 Linux）并安装。
2. 打开 Docker Desktop，等待其显示 **"Docker Desktop is running"**。

::: warning 保持 Docker 处于运行状态
每次启动应用时，Docker Desktop 都必须处于运行状态。如果它已关闭，
第 2 步中的命令会报 "cannot connect" 错误。
:::

## 第 2 步——启动应用

应用以两个现成的 Docker 镜像发布。两种方式任选其一；它们启动的是同一套
前端和后端。

### 方案 A——在 Docker Desktop 中操作（无需终端）

1. 在 Docker Desktop 顶部的**搜索栏**中搜索
   **`yongzwu/chronogeolab-backend`**，点击 **Pull**。
2. 再搜索 **`yongzwu/chronogeolab-frontend`**，同样点击 **Pull**。
3. 在 **Images** 标签页中，点击 **chronogeolab-backend** 旁边的 **Run**（▶）。
   在 **Optional settings** 中设置：
   - **Container name:** `cgl-backend`
   - **Host port:** `8000`
4. 对 **chronogeolab-frontend** 执行同样的操作，设置为：
   - **Container name:** `cgl-frontend`
   - **Host port:** `5173`

现在两个容器都会在 **Containers** 标签页中显示为 **Running**，之后你可以
在该页面启动或停止它们。

### 方案 B——两条命令

::: details 如何打开终端？
- **Windows：** 点击**开始**，输入 `powershell`，按回车。
- **Mac：** 按 **Cmd + Space**，输入 `Terminal`，按回车。
- **Linux：** 打开你的**终端**应用。

这些命令在任何目录下都能运行。
:::

依次运行以下命令：

```bash
docker run -d --name cgl-backend -p 8000:8000 yongzwu/chronogeolab-backend:latest
docker run -d --name cgl-frontend -p 5173:80 yongzwu/chronogeolab-frontend:latest
```

每条命令执行成功后会打印一个容器 ID。

::: tip 首次启动较慢
首次启动需要下载镜像，可能耗时几分钟。如果看到
**"name is already in use"**，说明容器已经存在——请改为在
**Containers** 标签页中启动它。
:::

## 第 3 步——打开应用

访问 <http://localhost:5173>，你应该会看到 **ChronoGeoLab** 的主界面。

![初始页面](/getting-started/initial-page.png)

## 第 4 步——运行你的第一个时空分析

我们将使用一个内置示例数据集：先把一条 GPS 轨迹可视化为 3D，
再基于它构建时空棱柱（Space-Time Prism）。

### 将轨迹可视化为 3D

1. **加载轨迹。** 下载
   <a href="/ChronoGeoLab/example_1.csv" download="example_1.csv">example_1.csv</a>
   ——一位用户一天的 GPS 轨迹（约 800 个点，一次 家 → 活动 → 家 的出行）。
   打开 **Data** 面板，选择 **Upload → CSV File** 并上传该文件。在
   **Map Coordinate Columns**（坐标列映射）步骤中，**longitude**、
   **latitude** 和 **altitude** 列会被自动识别；确认后完成即可。

   ![上传数据](/getting-started/data-source.png)
   ![映射坐标列](/getting-started/map-columns.png)

2. **选择工具。** 在 **Select Analysis Tool**（选择分析工具）界面中，
   选择 **3D Trajectory**。

   ![选择 3D Trajectory 工具](/getting-started/select-tool.png)

3. **检查日期时间列。** 应用会自动识别本示例中的 `dataTime` 列，
   保持默认即可。该字段定义了垂直方向的时间轴；使用自己的数据时，
   请选择存储时间戳的那一列。

   ![检查日期时间列](/getting-started/tool-setting.png)

4. **运行并探索。** 点击 **Run Analysis**，然后**按住鼠标右键拖拽**旋转地图，
   直到垂直时间轴进入视野。将鼠标悬停在任意点上即可查看该点的数值。

   ![可视化后的轨迹](/getting-started/visualized-trajectory.png)

### 构建时空棱柱

1. **设置锚点。** 在地图上点击家的位置放置**起始锚点**，再点击其中一个
   停留点放置**结束锚点**。棱柱将展示此人在这两个点之间可能到达的时空范围。

   ![选择家的位置作为起始锚点](/getting-started/select-home-anchor.png)
   ![选择一个活动停留点作为结束锚点](/getting-started/select-end-anchor.png)

2. **配置参数。** 点击 **Build Space-Time Prism**，设置面板会在右侧打开。
   本示例使用 **60 km/h** 的出行速度，速度真实度（Speed Realism）为
   **Free-flow**。如果想改用该用户的实际出行速度来近似，可将
   **Speed Realism** 切换为 **Auto**。

   ![时空棱柱设置](/getting-started/stp-tool-setting.png)

3. **运行。** 点击 **Run**。根据锚点区域和参数设置的不同，计算耗时从
   不到一分钟到几分钟不等。完成后，潜在停留时间的热力图会与 3D 棱柱视图
   一同呈现。

   ![时空棱柱结果](/getting-started/stp-result.png)

4. **进一步观察。** 点击地图左下角的 **Focused 3D View**。它会放大棱柱，
   并展示两个锚点之间每个时间切片上的潜在路径区域。按住右键拖拽可以改变
   视角，也可以点击播放按钮观看棱柱随时间变化的动画。

   ![Focused 3D View](/getting-started/stp-focused.png)

接下来，试试其他工具：
[时空核密度估计（STKDE）](/tools/stkde) 和
[时空立方体（Space-Time Cube）](/tools/space-time-cube)。
