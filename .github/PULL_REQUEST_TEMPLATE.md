## What & why

<!-- What does this PR change, and what problem does it solve? Link the issue if one exists. -->

## Validation

<!-- Check what you ran and paste failures if any. "Not run" is acceptable only with a reason. -->

- [ ] Frontend: `npm run build`
- [ ] Frontend: `npm run lint`
- [ ] Frontend: `npm test`
- [ ] Backend: `uv run pytest tests/ -v`
- [ ] Backend: `uv run ruff check .`
- [ ] Docs: `npm run docs:build`
- [ ] Ran the affected flow in the app (`npm run dev`)

Not run / failures:

## Contract changes

<!-- Delete this section if nothing below applies. -->

- [ ] API request/response shape changed → `docs/reference/api.md` updated
- [ ] Backend output fields changed → normalizer, TS interfaces, layer
      accessors/templates, and tests updated (see `docs/contributing/adding-a-tool.md`)
- [ ] Data-format or visualization behavior changed → docs under `docs/` updated

## AI assistance

<!-- Optional but appreciated: which agent/tool was used, if any. You are responsible for the diff either way. -->
