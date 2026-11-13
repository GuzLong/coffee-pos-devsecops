# coffee-pos-devsecops

A small coffee-shop POS API deployed to Azure by a fully automated, security-gated pipeline.
The app is the payload; the pipeline and infrastructure are the point.

> Status: Phase 0 — setup. Sections below fill in as each phase lands.

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
_TBD (Phase 1)_

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
