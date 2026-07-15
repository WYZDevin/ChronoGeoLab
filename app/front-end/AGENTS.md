# AGENTS.md

Frontend instructions for agents working under `app/front-end/`. Repo-wide
rules in `../../AGENTS.md` also apply. Only this app's responsibility and
rules live here — details are in the linked docs.

## Responsibility

The ChronoGeoLab browser interface: React 18, TypeScript, Vite, Redux
Toolkit, deck.gl 9, react-map-gl, maplibre-gl, Turf.js, Tailwind CSS,
Radix/shadcn UI, Vitest, and Playwright. It uploads CSV/GeoJSON trajectory
data, runs analysis tools in the browser or through the Flask backend,
normalizes results, and renders them on a deck.gl map.

## Rules

- Every tool declares `capabilities.executionPolicy` (`frontend_only`,
  `backend_only`, `hybrid`). The policy is the source of truth — resolve
  available modes only via `resolveToolCapabilities()` /
  `useResolvedCapabilities()`; never infer capability from tool name, dataset
  size, or backend availability, and never auto-switch modes without user
  awareness.
- The UI offers only the modes the resolver returns: `backend_only` tools
  show a runs-on-backend indicator and disable when the backend is offline;
  `hybrid` tools show a mode selector preselecting `defaultMode`.
- Rendering is mode-agnostic: normalized results render through the same
  path; never branch visualization on execution mode.
- Backend HTTP calls live only in `src/services/backend-api-service.ts`,
  which returns error objects or nulls instead of throwing into UI code.
- Construct deck.gl layers only in `src/services/layer-factory.ts`. Store
  serializable descriptors in Redux (never layer instances), keep layer IDs
  stable, and give every function accessor a matching `updateTriggers` entry.
- Use constants from `src/utils/constants.tsx` for processed field names —
  no hardcoded strings.
- Move computation exceeding ~50–100 ms on the main thread to a Web Worker
  (pure compute only, messages carry a `jobId`). Avoid O(N²) over raw
  features; prefer binning/indexing; cap grid/cell counts and warn when
  clamped.
- Match existing React/Redux/shadcn patterns; keep large arrays out of
  Redux when a cache/reference pattern exists; avoid broad UI rewrites and
  formatting churn.
- Before finishing: `npm run build`, `npm run lint`, `npm test`. For map or
  workflow E2E use `npx playwright test` with this directory's config (the
  root `tests/example.spec.ts` is only the Playwright starter sample). Bug
  fixes include a regression test when practical.

## Key Files

```text
src/interfaces/simple-tool.ts        Tool interfaces and execution policy types
src/services/analysis-engine.ts      Entry point for all tool runs
src/services/backend-api-service.ts  Only place for backend HTTP calls
src/services/execution-resolver.ts   Resolves frontend/backend availability
src/services/backend-normalizer.ts   Converts backend output to frontend shape
src/services/layer-factory.ts        Only place to construct deck.gl layers
src/tools/                           Browser tool implementations
src/utils/tool-registry.ts           Frontend tool registry
src/stores/                          Redux slices
src/components/                      UI and map components
src/visualization-templates/         Layer config templates
```

## Where To Look

| Task / question | Read |
|---|---|
| Add or update a tool (skeletons, normalizer, checklist) | `../../docs/contributing/adding-a-tool.md` |
| Execution data flow, services, Redux slices | `../../docs/reference/architecture.md` |
| Backend API contract | `../../docs/reference/api.md` |
| Configure or add a deck.gl layer | `../../.agent/skills/deckgl-layer-config.md` |
| Backend→frontend field mapping, normalizer structure | `../../.agent/skills/deckgl-data-pipeline.md` |
| Performance checklist (run before layer changes) | `../../.agent/skills/deckgl-performance.md` |
| Picking, hover, tooltips | `../../.agent/skills/deckgl-picking.md` |
| Visual baselines (GPU-sensitive — read before updating) | `../../.agent/skills/visual-regression.md` |
| Setup, env vars (`VITE_BACKEND_URL`, …), commands | `../../CONTRIBUTING.md`, `../../.env.example` |
