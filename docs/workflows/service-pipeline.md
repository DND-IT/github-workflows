---
title: Service Pipeline
---

## Description

End-to-end build and release pipeline for containerized services. Builds a
Docker image, publishes it to GHCR as a transient build-cache image, re-tags
and pushes to one or more ECR registries, publishes a GitHub release via
[action-releaser](https://github.com/DND-IT/action-releaser), deploys via
[action-deployer](https://github.com/DND-IT/action-deployer), and sends a
Slack notification.

**Pipeline flow:**

```
setup  ──►  build  ──►  tag-push  ──►  deploy  ──►  notify
  (plan release)    (per environment)   (publish release +
                                         deploy, or PR preview)
```

`cleanup` runs in parallel on PR `closed` events and removes `pr-{N}*` tags
from the PR preview environment's ECR.

### Release-gated contract

The `release` input controls when main-branch pushes advance ECR tags.

- `auto` (default): every main-branch commit whose message triggers a version
  bump (via conventional commits) publishes a release. Non-release commits
  (`chore:`, `docs:`, `refactor:` without `!`) still build the image into GHCR
  but do **not** push to ECR and do **not** advance `latest`.
- `gated`: main-branch commits open a release PR. The tags advance only when
  the release PR merges.

In both modes, a commit to main that does not trigger a release does not push
to ECR. This replaces the older "every main push advances latest" behaviour
from `@v3`.

### Tag ordering invariant

`tag-push` runs across every environment in the matrix before the GitHub
release is published. If any environment's push fails, the release is not
created — preserving the invariant "GitHub release exists ⇒ image is in every
ECR". The `release` step of the `deploy` job runs last, only after all
`tag-push` matrix legs succeed.

### PR preview deploys

On pull-request events the pipeline pushes the image to `pr_environment`
(defaults to `dev`) with tags `pr-{N}` and `pr-{N}-{sha}`, then invokes
`action-deployer` against `pr_environment` with version `pr-{N}`. When the PR
closes, `cleanup` removes the PR tags from that environment's ECR.

<!-- action-docs-inputs source=".github/workflows/service-pipeline.yaml" -->

<!-- action-docs-outputs source=".github/workflows/service-pipeline.yaml" -->

<!-- action-docs-usage source=".github/workflows/service-pipeline.yaml" project="dnd-it/github-workflows/.github/workflows/service-pipeline.yaml" version="v4" -->

## Prerequisites

- A `cliff.toml` at `service_path` (or at repo root for single-service repos)
  configuring [git-cliff](https://git-cliff.org/) for changelog generation.
  See [action-releaser](https://github.com/DND-IT/action-releaser) for the
  expected format.
- A `.github/matrix-config.yaml` defining environments. See
  [action-config](https://github.com/DND-IT/action-config) for the format.
- A GitHub App with `contents: write`, `issues: write`, `pull-requests: write`
  on the repo. Repository secret: `FISSION_GH_APP_PRIVATE_KEY`. Repository
  variable: `FISSION_GH_APP_ID`.
- Optional: `SLACK_BOT_TOKEN` for release notifications.

## Examples

### Minimal — single service repo

```yaml
name: backend

on:
  push:
    branches: [main]
    paths: ['backend/**']
  pull_request:
    paths: ['backend/**']
    types: [opened, synchronize, reopened, closed]
  workflow_dispatch:

jobs:
  pipeline:
    uses: DND-IT/github-workflows/.github/workflows/service-pipeline.yaml@v4
    with:
      service_name: social-media
      service_path: backend
      config_path: '.github/matrix-config.yaml'
      app_id: ${{ vars.FISSION_GH_APP_ID }}
    secrets:
      app_private_key: ${{ secrets.FISSION_GH_APP_PRIVATE_KEY }}
```

**Note:** include `closed` in the PR `types` so the cleanup job runs when PRs
close.

### With Slack notifications

```yaml
jobs:
  pipeline:
    uses: DND-IT/github-workflows/.github/workflows/service-pipeline.yaml@v4
    with:
      service_name: my-api
      service_path: .
      config_path: '.github/matrix-config.yaml'
      slack_channel: 'C09LG2L8EQ5'
      app_id: ${{ vars.FISSION_GH_APP_ID }}
    secrets:
      slack_bot_token: ${{ secrets.SLACK_BOT_TOKEN }}
      app_private_key: ${{ secrets.FISSION_GH_APP_PRIVATE_KEY }}
```

### Gated release strategy

```yaml
jobs:
  pipeline:
    uses: DND-IT/github-workflows/.github/workflows/service-pipeline.yaml@v4
    with:
      service_name: my-service
      release: gated
      config_path: '.github/matrix-config.yaml'
      app_id: ${{ vars.FISSION_GH_APP_ID }}
    secrets:
      app_private_key: ${{ secrets.FISSION_GH_APP_PRIVATE_KEY }}
```

Under `gated`, every release-worthy main-branch commit creates a release PR
(via `action-releaser` in `pr` mode). Merging the release PR publishes the
release and advances the version tag in ECR.

### Custom Dockerfile path

```yaml
jobs:
  pipeline:
    uses: DND-IT/github-workflows/.github/workflows/service-pipeline.yaml@v4
    with:
      service_name: my-service
      service_path: services/api
      dockerfile_path: docker/production.Dockerfile
      config_path: '.github/matrix-config.yaml'
      app_id: ${{ vars.FISSION_GH_APP_ID }}
    secrets:
      app_private_key: ${{ secrets.FISSION_GH_APP_PRIVATE_KEY }}
```

`dockerfile_path` is resolved relative to `service_path`.

### With Docker build secrets

```yaml
jobs:
  pipeline:
    uses: DND-IT/github-workflows/.github/workflows/service-pipeline.yaml@v4
    with:
      service_name: my-service
      config_path: '.github/matrix-config.yaml'
      app_id: ${{ vars.FISSION_GH_APP_ID }}
    secrets:
      app_private_key: ${{ secrets.FISSION_GH_APP_PRIVATE_KEY }}
      docker_secrets: |
        NPM_TOKEN=${{ secrets.NPM_TOKEN }}
        PIP_INDEX_URL=${{ secrets.PIP_INDEX_URL }}
```

```dockerfile
RUN --mount=type=secret,id=NPM_TOKEN \
    NPM_TOKEN=$(cat /run/secrets/NPM_TOKEN) npm ci
```

### Matrix config example

```yaml
settings:
  dimension: environment

global:
  aws_region: eu-central-1
  aws_iam_role_name: cicd-iac
  release: auto         # or 'gated'
  tag_prefix: v         # default; monorepo consumers override per-target

environment:
  dev:
    aws_account_id: "123456789012"
  prod:
    aws_account_id: "987654321098"
```

For monorepos, set `tag_prefix` per target (e.g., `my-service-v`) so each
service tags its releases distinctly.

## FAQ

### How are images tagged?

- Every build pushes a transient image to
  `ghcr.io/{owner}/{repo}/build-cache:{service}-{sha}`. This is the
  cross-job transport medium — downstream jobs pull from here.
- On PRs: the image is pushed to the `pr_environment`'s ECR with tags
  `pr-{N}` and `pr-{N}-{sha}`.
- On a main-branch commit that publishes a release: the image is pushed to
  every environment's ECR with the version tag (e.g., `1.7.3`) and `latest`.
- Non-release commits on main do not advance ECR tags (see the
  "release-gated contract" above).

### What cleans up the build-cache images in GHCR?

Call `docker-cleanup.yaml` in `prune-cache` mode on a schedule. Example:

```yaml
name: Prune GHCR build-cache

on:
  schedule:
    - cron: '0 3 * * *'

jobs:
  prune:
    uses: DND-IT/github-workflows/.github/workflows/docker-cleanup.yaml@v4
    with:
      mode: prune-cache
      max_age_days: 14
```

### Can I use this in a monorepo?

Yes. Set `service_path` to the subdirectory and set `tag_prefix` per target
in `matrix-config.yaml` so each service gets a distinct release tag prefix.

### Migrating from @v3

See the [migration guide](../getting-started/v3-to-v4-migration.md) for the
full breaking-change list.
