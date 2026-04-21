---
title: Docker Cleanup
---

<!-- action-docs-header source=".github/workflows/docker-cleanup.yaml" -->

## Description

Two modes for removing Docker images.

- **`pr-tags`** (default): deletes every tag matching `pr-{N}` or `pr-{N}-*`
  for a specific PR. Uses ECR when AWS credentials are passed, otherwise
  GHCR. Intended for PR close events, where it runs as the `cleanup` job in
  [service-pipeline](./service-pipeline.md).
- **`prune-cache`**: deletes GHCR package versions in the build-cache repo
  older than `max_age_days`. Intended for a scheduled invocation so the
  per-commit images produced by [docker-build](./docker-build.md) do not
  accumulate indefinitely in GHCR.

<!-- action-docs-inputs source=".github/workflows/docker-cleanup.yaml" -->

<!-- action-docs-usage source=".github/workflows/docker-cleanup.yaml" project="dnd-it/github-workflows/.github/workflows/docker-cleanup.yaml" version="v4" -->

## Examples

### Delete PR tags from ECR on PR close

```yaml
on:
  pull_request:
    types: [closed]

jobs:
  cleanup:
    uses: DND-IT/github-workflows/.github/workflows/docker-cleanup.yaml@v4
    with:
      mode: pr-tags
      image_name: my-service
      aws_account_id: "123456789012"
      aws_region: eu-central-1
      aws_role_name: cicd-iac
      pr_number: ${{ github.event.pull_request.number }}
```

### Delete PR tags from GHCR (no AWS)

Omit the AWS inputs and the GHCR deletion path runs.

```yaml
jobs:
  cleanup:
    uses: DND-IT/github-workflows/.github/workflows/docker-cleanup.yaml@v4
    with:
      mode: pr-tags
      image_name: my-service
      pr_number: ${{ github.event.pull_request.number }}
```

### Schedule GHCR build-cache pruning

Run daily at 03:00 UTC; keep the last 14 days of cache images.

```yaml
name: Prune GHCR build-cache

on:
  schedule:
    - cron: '0 3 * * *'
  workflow_dispatch:

jobs:
  prune:
    uses: DND-IT/github-workflows/.github/workflows/docker-cleanup.yaml@v4
    with:
      mode: prune-cache
      max_age_days: 14
```

`cache_repo` defaults to `{repo-name}/build-cache`; override if your cache
images live elsewhere.

## Permissions

- **pr-tags ECR**: the OIDC role needs `ecr:BatchDeleteImage` and
  `ecr:ListImages` on the target repository.
- **pr-tags GHCR** and **prune-cache**: the workflow uses `GITHUB_TOKEN` with
  `packages: write`. Deleting org-level package versions requires that the
  default token has `admin:packages` on the organisation; if your org
  restricts this, pass a PAT via the `ghcr_token` secret.
