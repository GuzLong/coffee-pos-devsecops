# coffee-pos-devsecops

[![CI](https://github.com/GuzLong/coffee-pos-devsecops/actions/workflows/ci.yml/badge.svg)](https://github.com/GuzLong/coffee-pos-devsecops/actions/workflows/ci.yml)

A small coffee-shop POS API deployed to Azure by a fully automated, security-gated pipeline.
The app is the payload; the pipeline and infrastructure are the point.

> Status: Phase 2 — CI. Sections below fill in as each phase lands.

## Live demo
_TBD (Phase 5)_ — `https://<subdomain>.duckdns.org`

## Architecture
_TBD (Phase 7)_ — Mermaid diagram in `docs/`.

Code path: push → PR → lint + test → security scans (gitleaks, CodeQL, Trivy) → merge →
build image to GHCR → SSH deploy to VM → `/health` check (rollback on fail) → Prometheus/Grafana alerts to Discord.

## Tech stack
| Area | Tools |
|---|---|
| App | Python 3.12, FastAPI, PostgreSQL, pytest, ruff |
| Containers | Docker (multi-stage, non-root), Docker Compose |
| CI/CD | GitHub Actions, GHCR |
| Security | gitleaks, CodeQL, Trivy, Dependabot |
| IaC | Terraform (azurerm), cloud-init |
| Runtime | Azure Linux VM, Caddy, DuckDNS |
| Monitoring | Prometheus, Grafana, node_exporter, Discord alerts |

## Run locally
Requires Docker.
```bash
cp .env.example .env        # then set POSTGRES_PASSWORD (URL-safe characters only)
docker compose up --build
```
- API docs: http://localhost:8000/docs
- Health: http://localhost:8000/health · Metrics: http://localhost:8000/metrics

Tests (no Docker needed; uses in-memory SQLite):
```bash
python -m venv .venv && .venv/bin/pip install -r app/requirements-dev.txt
cd app && ../.venv/bin/pytest && ../.venv/bin/ruff check .
```

### API
| Method | Path | Notes |
|---|---|---|
| GET | `/menu` | List menu items |
| POST | `/menu` | `{"name", "price"}`; 409 on duplicate name |
| POST | `/orders` | `{"items": [{"menu_item_id", "quantity"}]}`; total computed server-side |
| GET | `/orders/{id}` | |
| GET | `/health` | 200 if DB reachable, else 503 — used by deploy health check |
| GET | `/metrics` | Prometheus format |

## CI
[`.github/workflows/ci.yml`](.github/workflows/ci.yml) runs on every PR and push to `main`:
1. **lint-test** — `ruff check`, `ruff format --check`, `pytest`
2. **build** — `docker build` of `app/` (runs only if lint-test passes)

Branch protection on `main` requires both checks, so a failing test blocks the merge.

## Security controls
_TBD (Phase 3–4)_

## Results
_TBD (Phase 7)_ — deploy time, vulnerabilities found/fixed, image size, rebuild time.

## Repo layout
```
app/                FastAPI source and tests
infra/              Terraform and cloud-init
deploy/             docker-compose.prod.yml, Caddyfile, monitoring configs
.github/workflows/  ci.yml, security.yml, deploy.yml
docs/               architecture diagram, screenshots, decisions
```

## Decisions
See [docs/decisions.md](docs/decisions.md).
