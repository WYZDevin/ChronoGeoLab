# Contributing

ChronoGeoLab welcomes contributions from humans and AI coding agents alike —
bug fixes, new analysis tools, documentation, and demo datasets.

The authoritative contributor guide is
[`CONTRIBUTING.md`](https://github.com/WYZDevin/ChronoGeoLab/blob/main/CONTRIBUTING.md)
in the repository; this page summarizes the workflow.

## Ways to contribute

- **Report bugs or propose tools** via
  [GitHub issues](https://github.com/WYZDevin/ChronoGeoLab/issues) — use the
  *New tool proposal* template for analysis tools.
- **Fix or build** — fork, branch, and open a pull request.
- **Improve these docs** — every page has an "Edit this page on GitHub" link.

## Development setup

```bash
# Frontend
cd app/front-end
npm install
npm run dev          # http://localhost:5173

# Backend (Python >= 3.12 + uv)
cd app/back-end
uv sync
uv run flask --app app run -p 8000
```

Or, from the repo root, `npm install && npm run dev` starts both.

## Contributing with an AI agent

The repo follows the [AGENTS.md](https://agents.md) standard. The `AGENTS.md`
files are the source of truth for agent instructions, written as tables of
contents: each states the responsibility and hard rules for its directory up
front, then points to the detailed docs.

| Your agent | What to do |
|---|---|
| Codex, Cursor, Copilot coding agent, Jules, and most others | Nothing — they read `AGENTS.md` (root + nested) automatically. |
| Claude Code | Nothing — `CLAUDE.md` imports `AGENTS.md`. A `/sync-tool` command ships in `.claude/commands/`. |
| Anything else | Start your session with: *"Read `AGENTS.md` and the nested `AGENTS.md` files before making changes."* |

Keep all agent instructions in the `AGENTS.md` files — per-vendor rule files
(`.cursorrules`, `GEMINI.md`, …) are not accepted.

You are responsible for what your agent produces: review the diff, run the
validation checks, and fill in the PR template honestly.

## Adding a new analysis tool

Follow the [step-by-step playbook](/contributing/adding-a-tool) — it covers
the backend and frontend skeletons, registration, the response normalizer,
field-name conventions, tests, and documentation.

## Validation before a PR

| Area | Commands |
|------|----------|
| Frontend | `npm run build` · `npm run lint` · `npm test` |
| Backend | `uv run pytest tests/ -v` · `uv run ruff check .` |
| Docs | `npm run docs:build` (repo root) |

CI runs frontend lint/typecheck/tests and backend tests as blocking checks.
