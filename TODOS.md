# TODOS

## Infrastructure

### Pin action-releaser and action-deployer to stable tags

**What:** Pin `DND-IT/action-releaser` and `DND-IT/action-deployer` to a specific tag (e.g. `@v0.3.2`) in `.github/workflows/service-pipeline.yaml` instead of the floating `@v0`. Let Renovate handle bumps.

**Why:** `@v0` is an unstable major version. A breaking change in either action reaches every consumer of service-pipeline simultaneously on the next workflow run. Pinning gives us review-before-bump via Renovate and isolates breakages to explicit upgrades.

**Context:** Introduced in the `service-pipeline` branch v4 refactor. `service-pipeline.yaml:165` (action-releaser) and `service-pipeline.yaml:230` (action-deployer). Repo already uses Renovate (see `renovate.json`); it will pick up specific-tag pins automatically. Blocked on those actions reaching a stable `v1` tag, or on us deciding that a specific commit/tag of `v0` is our pin point.

**Effort:** S
**Priority:** P2
**Depends on:** action-releaser and action-deployer publishing a stable tag (or us pinning to a specific `v0.x` commit).
