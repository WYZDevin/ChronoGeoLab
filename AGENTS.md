# AGENTS.md

Instructions for coding agents working on ChronoGeoLab — a monorepo for
time-geographic visualization and geospatial analysis. This file is a table
of contents: only repo-wide responsibilities and rules live here; details
live in the linked docs. Nested `AGENTS.md` files apply to their directories.

**The `AGENTS.md` files are the source of truth for agent instructions.** The
`CLAUDE.md` files only import them; if any other document conflicts, the
`AGENTS.md` file wins. Keep it that way: put new instructions in the linked
docs and add a pointer here — do not grow this file into a manual, and do not
add per-vendor rule files (`.cursorrules`, `GEMINI.md`, `.windsurf/`, …).

## Project Shape

```text
app/front-end/   React + TypeScript + Vite + Redux + deck.gl/maplibre
app/back-end/    Flask + Python 3.12 + GeoPandas/Shapely
docs/            VitePress documentation
demo-datasets/   Sample trajectory data
```

The frontend and backend are independent applications connected only by the
HTTP API.

## Rules

- Never import code across the frontend/backend boundary.
- The API contract (`docs/reference/api.md`) is the boundary: backend output
  changes must ripple through the frontend normalizer, TypeScript interfaces,
  layer accessors/templates, tests, and docs — in the same change.
- Keep public API and data-format changes backward compatible unless the task
  explicitly asks for a breaking change.
- Current state (since 2026-06): all analysis tools are temporarily
  `backend_only`; the browser implementations remain in place (revert via
  `executionPolicy` in `stkde-tool.ts` / `time-geography-tool.ts`).
- Keep diffs focused on the task; run `git status --short` first and preserve
  unrelated user changes. Don't edit generated or vendored files
  (`node_modules/`, `dist/`, docs build output) or lockfiles unless
  dependencies actually changed. Avoid new dependencies unless justified.
- Think before coding; simplicity first; surgical changes; goal-driven
  execution (full guidelines: `.agent/skills/karpathy-guidelines.md`).
- Validate what you changed (commands in the nested guides); if a check
  cannot run, say why and state the residual risk.
- Update docs when user-facing behavior, setup, data formats, tool options,
  API responses, or deployment change.

## Where To Look

| Task / question | Read |
|---|---|
| Frontend work (`app/front-end/`) | `app/front-end/AGENTS.md` |
| Backend work (`app/back-end/`) | `app/back-end/AGENTS.md` |
| Adding or updating an analysis tool | `docs/contributing/adding-a-tool.md` |
| API contract (canonical) | `docs/reference/api.md` |
| Architecture, data flow, key modules | `docs/reference/architecture.md` |
| Setup, dev commands, validation, PR expectations | `CONTRIBUTING.md` |
| deck.gl layers / data pipeline / performance / picking | `.agent/skills/deckgl-*.md` |
| Visual regression (Playwright baselines) | `.agent/skills/visual-regression.md` |
| Coding guidelines (full version) | `.agent/skills/karpathy-guidelines.md` |
| Deployment | `DEPLOY.md`, `docs/reference/deployment.md` |
| User-facing docs to update with behavior changes | `README.md`, `docs/guide/`, `docs/tools/` |
