# Adding or Updating a Tool

This is the canonical playbook for adding a new analysis tool to ChronoGeoLab
or changing an existing one. It applies to human contributors and to coding
agents — if you are pointing an AI assistant at this repo, have it follow this
page step by step.

## How tools work

A **tool** is a unit of geospatial analysis (e.g. STKDE, Space-Time Prism,
Buffer). Tools exist in two independent registries:

| Side | Implementation | Registry |
|------|----------------|----------|
| Frontend (browser) | `app/front-end/src/tools/<tool-name>-tool.ts` | `app/front-end/src/tools/index.ts` |
| Backend (Flask) | `app/back-end/app/tools/<tool_name>.py` | `app/back-end/app/tool_registry.py` |

Three hard rules:

1. **The tool `id` must match exactly on both sides.** The execution resolver
   and the backend API client route by this ID.
2. **Every frontend tool declares `capabilities.executionPolicy`** —
   `frontend_only`, `backend_only`, or `hybrid`. The policy is the source of
   truth; never infer capability from tool name, dataset size, or backend
   availability.
3. **Visualization is mode-agnostic.** Results render through the same path
   regardless of where they were computed. Never branch rendering logic on
   execution mode.

## Step 0 — Choose the execution policy

- `frontend_only` — runs in the browser only. No backend work needed.
- `backend_only` — runs on Flask only. The frontend needs a registration stub
  so the tool appears in the UI.
- `hybrid` — implemented on both sides; the user picks where it runs.

## Step 1 — Backend implementation

Skip this step for `frontend_only` tools.

Create `app/back-end/app/tools/<tool_name>.py`:

```python
import geopandas as gpd
from .base import BaseTool

class MyTool(BaseTool):
    @property
    def id(self) -> str:
        return "my-tool"  # must match the frontend tool id exactly

    @property
    def name(self) -> str:
        return "My Tool"

    @property
    def description(self) -> str:
        return "One-sentence description shown in the UI."

    # Default policy is "hybrid"; override if needed:
    # @property
    # def execution_policy(self) -> str:
    #     return "backend_only"

    def execute(
        self,
        gdf: gpd.GeoDataFrame,
        options: dict,
        attributes: dict,
    ) -> list[gpd.GeoDataFrame]:
        # All geospatial math happens here (GeoPandas/Shapely/NumPy/SciPy).
        return [result_gdf]
```

Then:

1. Register the class in `app/back-end/app/tool_registry.py` →
   `_register_all()`.
2. Return output geometries in **EPSG:4326**. The route handler converts
   GeoDataFrames to GeoJSON and builds the response envelope automatically —
   keep `routes.py` untouched.
3. Store any user-facing warnings in `GeoDataFrame.attrs["warnings"]`.
4. Use `_processed_*` field names from `app/back-end/app/constants.py` for
   computed output fields (see the field-name table below).
5. Add pytest coverage in `app/back-end/tests/` asserting the response shape,
   `runMeta.summary.bbox` (historically the #1 integration failure), warnings,
   and error behavior.

The full request/response/error contract is in the
[Backend API reference](../reference/api.md).

### Porting frontend logic to Python

Common Turf.js → GeoPandas/Shapely translations:

| Frontend (Turf.js) | Backend (Shapely/GeoPandas) |
|--------------------|-----------------------------|
| `turf.buffer(feature, dist, {units})` | `gdf.to_crs(utm).buffer(dist_meters)` |
| `turf.union(a, b)` | `shapely.ops.unary_union(geometries)` |
| `turf.intersect(a, b)` | `gdf1.overlay(gdf2, how='intersection')` |
| `turf.bbox(fc)` | `gdf.total_bounds` |
| `feature.geometry.coordinates` | `gdf.geometry.x`, `gdf.geometry.y` |
| `new Date(ts).getTime()` | `pd.to_datetime(col).astype(int) // 10**6` |

## Step 2 — Frontend implementation

Every tool needs a frontend class — a full implementation for
`frontend_only`/`hybrid`, or a registration stub for `backend_only`.

Create `app/front-end/src/tools/<tool-name>-tool.ts`:

```typescript
import { SimpleTool, ToolOptionSchema } from '@/interfaces/simple-tool';
import { FeatureCollection } from '@/interfaces/data-interfaces';
import { AttributeMapping } from '@/interfaces/attribute-mapping';

export class MyTool implements SimpleTool {
  id = 'my-tool';                    // must match the backend tool id exactly
  name = 'My Tool';
  description = 'One-sentence description shown in the UI.';
  icon = '🛠️';
  category = 'analysis' as const;    // 'visualization' | 'analysis' | 'processing'
  version = '1.0.0';
  capabilities = {
    executionPolicy: 'hybrid' as const,
    defaultMode: 'frontend' as const,   // only meaningful for 'hybrid'
  };

  // Only declare if the tool binds dataset fields (e.g. a time column)
  attributeMapping?: AttributeMapping;

  getOptionSchema(): ToolOptionSchema[] {
    // Options the UI renders; keys must match what the backend reads
    return [];
  }

  async analyze(
    data: FeatureCollection,
    options: Record<string, unknown>,
    attributes?: AttributeMapping
  ): Promise<FeatureCollection[]> {
    // Browser implementation. For backend_only stubs, throw instead:
    // throw new Error('My Tool requires the backend server.');
    return [result];
  }
}
```

Then:

1. Register it in `app/front-end/src/tools/index.ts` (import + add to
   `availableTools`).
2. For `backend_only` stubs: do **not** implement `analyze()` logic — throw a
   clear "requires the backend" error.
3. Add a normalizer case in
   `app/front-end/src/services/backend-normalizer.ts` if the backend output
   uses `_processed_*` fields or needs a custom deck.gl layer config. Simple
   polygon tools can fall through to `normalizeGeneric()` — optionally add the
   tool ID to the `labels` map in `createGenericPolygonLayerConfig()` for a
   nicer default layer label.
4. Construct deck.gl layers only via `src/services/layer-factory.ts`; add a
   template under `src/visualization-templates/` if the tool has its own layer
   defaults. Follow `.agent/skills/deckgl-layer-config.md`.
5. Use constants from `src/utils/constants.tsx` for processed field names —
   never hardcode the strings.
6. Add Vitest coverage — for backend-connected tools, test
   `normalizeBackendResponse()` with a mocked raw response.

### Field-name convention

The backend outputs `_processed_*` fields (defined in
`app/back-end/app/constants.py`); the frontend normalizer remaps them to
frontend names (defined in `app/front-end/src/utils/constants.tsx`):

| Backend field | Frontend field |
|---------------|----------------|
| `_processed_time` | `_time_order` |
| `_processed_height` | `_height` |
| `_processed_neighbors` | `_neighbors` |

## Step 3 — Keep both sides in sync

If a backend output field is added, renamed, or removed, update **all** of:

- the normalizer in `backend-normalizer.ts`,
- the TypeScript interfaces in `src/interfaces/`,
- the layer accessors/templates (`layer-factory.ts`,
  `visualization-templates/`),
- tests on both sides,
- the docs listed below.

Claude Code users can run the `/sync-tool` command
(`.claude/commands/sync-tool.md`), which automates the
backend↔frontend sync checklist.

## Step 4 — Verify

```bash
# Backend
cd app/back-end
uv run pytest tests/ -v
uv run ruff check .

# Frontend
cd app/front-end
npm run build        # tsc + vite build
npm run lint
npm test             # Vitest
```

Then run the app (`npm run dev` at the repo root) and execute the tool
end-to-end on a demo dataset from `demo-datasets/` — confirm the layer
renders and the tooltip shows sensible fields.

## Step 5 — Document

- Add or update the tool page under `docs/tools/` (user-facing usage +
  a separate `<tool>-algorithm.md` page if the method is nontrivial), and add
  it to the sidebar in `docs/.vitepress/config.mts`.
- Update `docs/reference/api.md` if the API contract changed.
- Note the change in your PR description, including which validation commands
  you ran.
