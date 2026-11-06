"""Small offline calculations to exercise native libraries inside the bundle."""

import json
from urllib.request import Request, urlopen


def check_analysis(url):
    points = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [lng, lat]},
                "properties": {"timestamp": timestamp},
            }
            for lng, lat, timestamp in (
                (-122.4194, 37.7749, "2025-01-15T10:00:00Z"),
                (-122.4094, 37.7849, "2025-01-15T10:05:00Z"),
                (-122.3994, 37.7949, "2025-01-15T10:10:00Z"),
            )
        ],
    }
    for tool in ("time-geography", "space-time-cube", "stkde", "space-time-prism"):
        payload = {"data": points, "attributes": {"time": "timestamp"}}
        if tool == "space-time-prism":
            payload["options"] = {
                "analysisMode": "interactive",
                "_anchorA": {"lng": -83.740, "lat": 42.280,
                             "timestamp": "2024-01-01T09:00:00Z"},
                "_anchorB": {"lng": -83.735, "lat": 42.281,
                             "timestamp": "2024-01-01T10:00:00Z"},
                "speedMode": "walking", "timeSlices": 8, "showPPA": True,
            }
        request = Request(
            f"{url}/api/v1/tools/{tool}/execute",
            data=json.dumps(payload).encode(),
            headers={"Content-Type": "application/json"},
        )
        with urlopen(request, timeout=60) as response:
            result = json.load(response)
        if not result.get("success") or not any(
            output.get("features") for output in result.get("outputs", [])
        ):
            raise RuntimeError(f"Bundled analysis failed: {tool}: {result}")
