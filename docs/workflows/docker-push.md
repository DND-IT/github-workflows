---
title: Docker Push
---

<!-- action-docs-header source=".github/workflows/docker-push.yaml" -->

## Description

Pulls a pre-built image from GHCR and tags + pushes it to one or more
registries (ECR via OIDC, or GHCR directly). Used as the "tag-push" stage of
[service-pipeline](./service-pipeline.md), but callable directly for custom
flows.

Tags applied:

- `latest` when pushing from the default branch
- `version_tag` if non-empty (e.g. a release version)
- `prerelease_tag` if non-empty (e.g. `1.7.3-rc.pr42`)
- Each line of `additional_tags` (e.g. `short-sha`, `pr-{N}`)

<!-- action-docs-inputs source=".github/workflows/docker-push.yaml" -->

<!-- action-docs-usage source=".github/workflows/docker-push.yaml" project="dnd-it/github-workflows/.github/workflows/docker-push.yaml" version="v4" -->

## Examples

### Push to ECR with OIDC role

```yaml
jobs:
  push:
    uses: DND-IT/github-workflows/.github/workflows/docker-push.yaml@v4
    with:
      image_name: my-service
      image_ref: ghcr.io/my-org/my-repo/build-cache:my-service-abc1234
      aws_account_id: "123456789012"
      aws_region: eu-central-1
      aws_role_name: cicd-iac
      version_tag: "1.7.3"
      additional_tags: |
        abc1234
```

### Push to GHCR only (no AWS)

Omit the AWS inputs; the workflow falls through to GHCR re-tagging.

```yaml
jobs:
  push:
    uses: DND-IT/github-workflows/.github/workflows/docker-push.yaml@v4
    with:
      image_name: my-service
      image_ref: ghcr.io/my-org/my-repo/build-cache:my-service-abc1234
      version_tag: "1.7.3"
```
