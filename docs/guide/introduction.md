# Introduction

**ChronoGeoLab** helps you explore GPS movement data as interactive
3D space-time visualizations. Upload a trajectory, choose an analysis tool, and
inspect where movement happened, when it happened, and what places were
reachable between known points.

The app is built with [React](https://react.dev/), [deck.gl](https://deck.gl/),
and [MapLibre](https://maplibre.org/) in the browser. A required local
[Flask](https://flask.palletsprojects.com/) and
[GeoPandas](https://geopandas.org/) backend runs the analysis tools in the
current release, including road-network space-time prisms.

## Who is it for?

- **Researchers** studying human mobility, accessibility, and exposure.
- **Analysts** who want to visualize GPS trajectories without writing code.
- **Students** learning time-geography concepts such as paths, prisms, and
  density surfaces.

## What makes it different

- **Runs locally.** In the standard setup, uploaded data travels only between
  your browser and the Flask service on your computer.
- **Uses true 3D space-time.** X is longitude, Y is latitude, and Z is time.
  You can rotate the map to see how movement changes through the day.
- **Supports exploration.** Animate results, hover for values, drop pins, and
  place prism anchors directly on the map.

## The toolset at a glance

| Tool | What it answers |
|------|-----------------|
| [3D Trajectory](/tools/trajectory-3d) | *Where and when did the subject move?* |
| [Space-Time Kernel Density](/tools/stkde) | *Where and when does activity concentrate?* |
| [Space-Time Cube](/tools/space-time-cube) | *What was the environmental exposure along the path?* |
| [Space-Time Prism](/tools/space-time-prism) | *Where could the subject have been between two points?* |

## Privacy and network access

Trajectory analysis is local in the standard Docker setup, but the map is not
fully offline. CARTO, Esri, or Mapbox receives normal map-tile requests, and a
road-network prism can query public OpenStreetMap Overpass services for roads in
the selected area. Configure private equivalents before using sensitive study
locations in an environment where those requests are not acceptable.

::: tip Next steps
New here? Start with [Getting Started](/guide/getting-started). If the theory is
new to you, read [Core Concepts](/guide/concepts) first.
:::
