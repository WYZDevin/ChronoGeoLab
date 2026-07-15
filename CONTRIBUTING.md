# Contributing to ChronoGeoLab

Thanks for contributing! ChronoGeoLab welcomes pull requests from humans and
from AI coding agents alike — the rules below apply to both.

## Project layout

```
app/front-end/   React + TypeScript + Vite + Redux + deck.gl (browser app)
app/back-end/    Flask + Python 3.12 + GeoPandas (analysis API)
docs/            VitePress documentation site
```

The two apps are independent and communicate only over the HTTP API
(canonical contract: `docs/reference/api.md`).

## Contributing with an AI agent

This repo works with any coding agent via the [AGENTS.md](https://agents.md)
standard. **`AGENTS.md` is the single source of truth** for agent
instructions; nested guides (`app/front-end/AGENTS.md`,
`app/back-end/AGENTS.md`) apply to their directories.

- **Most agents** (Codex, Cursor, Copilot coding agent, Jules, and others)
  read `AGENTS.md` automatically — no setup needed.
- **Claude Code** reads `CLAUDE.md`, which simply imports `AGENTS.md`.
- **Any other agent:** start your session with
  *"Read `AGENTS.md` and the nested `AGENTS.md` files before making changes."*
  That is the only setup any agent needs — please don't add per-vendor rule
  files; keep everything in `AGENTS.md`.

Rules that agents will need along the way:

- Tool changes must follow the step-by-step playbook in
  `docs/contributing/adding-a-tool.md`.
- Project-specific deck.gl and testing playbooks live in `.agent/skills/`
  (plain markdown, referenced from `AGENTS.md` — readable by any agent).
- Claude Code users additionally get a `/sync-tool` command
  (`.claude/commands/`); other agents achieve the same by being asked to
  follow the playbook.

You are responsible for what your agent produces: review the diff, run the
validation commands, and fill in the PR template honestly.

## Development setup

```bash
# Frontend
cd app/front-end
npm install
npm run dev          # http://localhost:5173

# Backend (requires Python >= 3.12 and uv)
cd app/back-end
uv sync
uv run flask --app app run -p 8000
```

Or from the repo root: `npm install && npm run dev` starts both, and
`docker compose up --build` runs the full stack in containers. Docs:
`npm run docs:dev` / `npm run docs:build`.

Environment: copy `.env.example` to `app/front-end/.env` if you need local
config. `VITE_BACKEND_URL` defaults to `http://localhost:8000`;
`VITE_MAPBOX_API_KEY` is optional (non-satellite basemaps work without it).

## Validation before opening a PR

Run the checks relevant to what you touched:

| Area | Commands |
|------|----------|
| Frontend | `npm run build` · `npm run lint` · `npm test` |
| Backend | `uv run pytest tests/ -v` · `uv run ruff check .` |
| Docs | `npm run docs:build` (repo root) |

CI runs frontend lint/typecheck/tests and backend tests as blocking checks
(backend ruff is currently advisory).

## Pull request expectations

- Keep the PR focused on one issue or task.
- Summarize what changed and why; list the validation commands you ran and
  their results; call out anything you could not run.
- Explicitly flag API, data-format, or visualization-contract changes.
- Update docs when user-facing behavior, tool options, data formats, or API
  responses change.

## Proposing a new tool

Open an issue with the "New tool proposal" template before writing code —
it captures the tool ID, options, and execution policy in the shape the
implementation playbook consumes.

## License

By contributing you agree that your contributions are licensed under the
[MIT License](LICENSE).
