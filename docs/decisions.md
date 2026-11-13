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

## Measurements
| Metric | Value | Date |
|---|---|---|
| Manual deploy time (before Phase 5) | | |
| Pipeline deploy time | | |
| Image size: single-stage → multi-stage | | |
| Trivy / CodeQL findings: first run → fixed | | |
| Terraform full rebuild time | | |
