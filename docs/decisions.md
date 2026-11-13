# Decisions & measurements

Each phase: what was chosen, what was rejected, why. Record numbers when measured — they can't be recovered later.

## Phase 0 — Setup

| Chosen | Rejected | Why |
|---|---|---|
| Single VM + Docker Compose | Kubernetes (AKS) | Cheap, every part explainable in an interview; K8s is the next project |
| GitHub Actions + GHCR | Azure DevOps / ACR | Free for public repos, reviewers can open the Actions tab |
| Caddy + DuckDNS | Nginx + certbot | Automatic HTTPS with one config file |
| Discord webhook alerts | LINE Notify | LINE Notify has been shut down |

### Branch protection (set manually on GitHub)
Settings → Branches → Add branch ruleset (or classic rule) for `main`:
1. Require a pull request before merging (approvals: 0 — solo project).
2. Require status checks to pass — add the CI checks after Phase 2 first runs.
3. Block force pushes; restrict deletions.
4. Do not allow bypassing the above settings (applies to admins too).

Verify: `git push origin main` directly should be rejected.

## Phase 1 — App + Docker

| Chosen | Rejected | Why |
|---|---|---|
| SQLAlchemy `create_all` at startup | Alembic migrations | Schema is tiny and unreleased; add Alembic once it changes after first deploy |
| SQLite in-memory for unit tests | Postgres in tests | Tests run in <1s with no Docker; Postgres compatibility proven by `docker compose up` |
| `prometheus-fastapi-instrumentator` | Hand-written `prometheus_client` middleware | One line gives request count/latency per route |
| Multi-stage build, venv copied to `python:3.12-slim`, UID 10001 | Single-stage, root user | Smaller image, no pip/build tools at runtime, container escape doesn't land as root |
| `/health` checks the DB | Static 200 | Deploy rollback (Phase 5) should trigger when the app can't reach its DB |
| Order stores `unit_price` per line; total computed server-side | Trust client total | Client can't set its own price; old orders keep historical prices |
| Compose binds API to `127.0.0.1` only | `0.0.0.0` | Local dev shouldn't be reachable from the LAN; Caddy fronts it in prod |

Known gap: `POST /menu` has no auth yet — anyone can add menu items once deployed. Revisit before Phase 5.

## Measurements
| Metric | Value | Date |
|---|---|---|
| Manual deploy time (before Phase 5) | | |
| Pipeline deploy time | | |
| Image size: naive single-stage (`python:3.12`, root) → multi-stage (`3.12-slim`, non-root) | 1.73 GB → 275 MB (−84%); most of the cut is the slim base | 2026-11-13 |
| Trivy / CodeQL findings: first run → fixed | | |
| Terraform full rebuild time | | |
