# AGENTS.md

Backend instructions for agents working under `app/back-end/`. Repo-wide
rules in `../../AGENTS.md` also apply. Only this app's responsibility and
rules live here — details are in the linked docs.

## Responsibility

The ChronoGeoLab stateless Flask API: receives GeoJSON tool execution
requests, converts them to GeoDataFrames, computes with
GeoPandas/Shapely/NumPy/SciPy, and returns GeoJSON plus execution metadata.
Python ≥ 3.12; dependencies managed with `uv` (`uv.lock`).

## Rules

- Stateless: no database, no persistent server state.
- Keep route handlers thin — geospatial work belongs in tools or utilities,
  never in `routes.py`.
- Tools are stateless `BaseTool` subclasses registered in
  `app/tool_registry.py`; `execute()` returns `list[GeoDataFrame]`.
- Responses must match the contract in `docs/reference/api.md` exactly —
  especially `runMeta.summary.bbox`, historically the #1 frontend
  integration failure.
- Convert output geometries to EPSG:4326 before returning GeoJSON; keep
  warnings in `GeoDataFrame.attrs["warnings"]`; use `_processed_*` field
  names from `app/constants.py`.
- `researchArea` is optional; route logic may pass it privately to tools as
  `_researchArea`, but `runMeta.params` must echo only user-facing options.
- Python 3.12 typing style; stay compatible with the Pydantic models in
  `app/models.py`; don't rename API fields unless the frontend contract is
  updated in the same change; don't mass-format unrelated files.
- Before finishing: `uv run pytest tests/ -v` and `uv run ruff check .`.
  API/tool changes assert response shape, bbox, warnings, and error
  behavior; bug fixes include a regression test when practical.

## Key Files

```text
app/__init__.py       Flask app factory
app/routes.py         API routes under /api/v1
app/models.py         Pydantic request/response contracts
app/tool_registry.py  Tool registry
app/utils.py          GeoJSON/GeoDataFrame conversion and response helpers
app/tools/base.py     BaseTool contract
app/tools/            Tool implementations
tests/                Pytest suite
```

## Where To Look

| Task / question | Read |
|---|---|
| API contract: request/response/error shapes (canonical) | `../../docs/reference/api.md` |
| Add or update a tool (skeleton, registration, tests) | `../../docs/contributing/adding-a-tool.md` |
| Architecture and module responsibilities | `../../docs/reference/architecture.md` |
| Setup and dev commands (`uv sync`, run server, tests) | `../../CONTRIBUTING.md` |
