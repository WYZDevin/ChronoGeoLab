# Changelog

All notable user-facing changes to ChronoGeoLab are documented here.

## 1.0.1 — 2026-07-22

### Fixed

- Restored backend startup by making the road-network prism self-contained;
  v1.0.0 referenced a Python module that was missing from the release.
- Made Playwright start the Flask API as well as Vite, so the tested workflow
  matches the current `backend_only` execution policy.
- Corrected setup, architecture, environment, privacy, and update documentation
  to reflect that all analysis tools currently require the backend.

### Changed

- Added release validation before Docker images can be published and added both
  plain and `v`-prefixed semantic-version image tags.
- Updated the frontend build and CI runtime to supported Node.js 24.
- Removed unused frontend packages and refreshed locked dependencies to reduce
  known security advisories.
- Aligned package metadata and citation information on version 1.0.1 and the MIT
  license.
