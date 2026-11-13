# coffee-pos-devsecops

## What this is
A portfolio project for a DevSecOps / Cloud junior role. A small coffee-shop
POS API is the payload; the real deliverable is the pipeline and infrastructure
around it. Owner is a CS undergraduate learning these tools, so explain what
you did and why after each change, in Thai, briefly.

## Stack (do not swap without asking)
- App: Python 3.12, FastAPI, PostgreSQL, pytest, ruff
- Containers: Docker multi-stage, non-root user, Docker Compose
- CI/CD: GitHub Actions, images pushed to GHCR
- Security: gitleaks, CodeQL, Trivy (image + IaC), Dependabot
- IaC: Terraform (azurerm), remote state in Azure Storage, cloud-init
- Runtime: one Azure Linux VM, Caddy for HTTPS, DuckDNS domain
- Monitoring: Prometheus, Grafana, node_exporter, alerts to Discord webhook

## Repo layout
```
app/                FastAPI source and tests
infra/              Terraform and cloud-init
deploy/             docker-compose.prod.yml, Caddyfile, monitoring configs
.github/workflows/  ci.yml, security.yml, deploy.yml
docs/               architecture diagram, screenshots, decisions
```

## Rules
- Work on one phase at a time (see Phases). Stop when its done-criteria pass.
- Small commits with clear messages; one feature branch and one PR per task.
- Never commit secrets. Never ask the owner to paste a secret into chat.
  Use .env (gitignored) locally and GitHub Actions Secrets in CI.
- Never run `terraform apply` or `terraform destroy` yourself. Run
  `terraform plan`, show the result, and let the owner apply.
- Pin versions of actions, base images and providers.
- Every phase ends by updating README.md and docs/decisions.md
  (what was chosen, what alternative was rejected, why).

## Phases and done-criteria
0 Setup: repo skeleton, .gitignore, README outline, branch protection notes.
1 App + Docker: menu and order endpoints, /health, /metrics, tests pass,
  `docker compose up` serves the API.
2 CI: lint, test and image build on every PR; failing tests block merge.
3 Security: gitleaks, CodeQL, Trivy, Dependabot; pipeline fails on HIGH+.
4 Infra: Terraform creates VM, network, NSG (22, 80, 443 only); cloud-init
  disables password SSH, enables ufw and fail2ban.
5 CD: merge to main builds, pushes to GHCR, deploys over SSH, checks /health,
  rolls back to previous image tag on failure.
6 Monitoring: Prometheus + Grafana dashboard, alert on app down and disk >80%.
7 Polish: full README, architecture diagram, measured numbers.
