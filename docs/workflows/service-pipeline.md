---
title: Service Pipeline
---

## Description

End-to-end build and release pipeline for containerized services. Builds a Docker image, pushes to ECR across multiple AWS environments, creates a GitHub release via semantic-release, and sends a Slack notification.

**Pipeline flow:** Setup → Build → Release Info (dry-run) → Push (per environment) → Create Release → Notify Slack

<!-- action-docs-inputs source=".github/workflows/service-pipeline.yaml" -->

<!-- action-docs-outputs source=".github/workflows/service-pipeline.yaml" -->

<!-- action-docs-usage source=".github/workflows/service-pipeline.yaml" project="dnd-it/github-workflows/.github/workflows/service-pipeline.yaml" version="v3" -->

## Prerequisites

- A `.releaserc.json` at the repo root (or `service_path`) excluding the `@semantic-release/npm` plugin. See [gh-release](./gh-release.md) for details.
- A `.github/matrix-config.yaml` defining AWS environments. See [action-config](https://github.com/DND-IT/action-config) for the format.
- Repository secrets: `FISSION_GH_APP_PRIVATE_KEY`, `SLACK_BOT_TOKEN`
- Repository variables: `FISSION_GH_APP_ID`

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
  workflow_dispatch:

jobs:
  pipeline:
    uses: DND-IT/github-workflows/.github/workflows/service-pipeline.yaml@v3
    with:
      service_name: social-media
      service_path: backend
      config_path: '.github/matrix-config.yaml'
      app_id: ${{ vars.FISSION_GH_APP_ID }}
    secrets:
      app_private_key: ${{ secrets.FISSION_GH_APP_PRIVATE_KEY }}
```

### With Slack notifications

```yaml
jobs:
  pipeline:
    uses: DND-IT/github-workflows/.github/workflows/service-pipeline.yaml@v3
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

### Custom Dockerfile path

```yaml
jobs:
  pipeline:
    uses: DND-IT/github-workflows/.github/workflows/service-pipeline.yaml@v3
    with:
      service_name: my-service
      service_path: services/api
      dockerfile_path: docker/production.Dockerfile
      config_path: '.github/matrix-config.yaml'
      app_id: ${{ vars.FISSION_GH_APP_ID }}
    secrets:
      app_private_key: ${{ secrets.FISSION_GH_APP_PRIVATE_KEY }}
```

### With Docker build secrets

Use `docker_secrets` to pass secrets into the Docker build (e.g., private registry tokens). In your Dockerfile, mount them with `RUN --mount=type=secret`:

```yaml
jobs:
  pipeline:
    uses: DND-IT/github-workflows/.github/workflows/service-pipeline.yaml@v3
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

Then in your `Dockerfile`:

```dockerfile
RUN --mount=type=secret,id=NPM_TOKEN \
    NPM_TOKEN=$(cat /run/secrets/NPM_TOKEN) npm ci
```

### With custom build arguments

Use `docker_build_args` to pass additional build arguments beyond the built-in `VERSION`, `BUILD_DATE`, and `VCS_REF`:

```yaml
jobs:
  pipeline:
    uses: DND-IT/github-workflows/.github/workflows/service-pipeline.yaml@v3
    with:
      service_name: my-service
      config_path: '.github/matrix-config.yaml'
      app_id: ${{ vars.FISSION_GH_APP_ID }}
      docker_build_args: |
        NODE_ENV=production
        API_BASE_URL=https://api.example.com
    secrets:
      app_private_key: ${{ secrets.FISSION_GH_APP_PRIVATE_KEY }}
```

### Matrix config example

The `config_path` file should follow the [action-config](https://github.com/DND-IT/action-config) format:

```yaml
environments:
  - dev
  - prod

config:
  dev:
    aws_account_id: "123456789012"
    aws_region: eu-central-1
    aws_iam_role_name: cicd-iac
  prod:
    aws_account_id: "987654321098"
    aws_region: eu-central-1
    aws_iam_role_name: cicd-iac
```

### `.releaserc.json` example

```json
{
  "branches": ["main"],
  "plugins": [
    [
      "@semantic-release/commit-analyzer",
      {
        "preset": "conventionalcommits",
        "releaseRules": [
          { "type": "feat", "release": "minor" },
          { "type": "fix", "release": "patch" },
          { "breaking": true, "release": "major" }
        ]
      }
    ],
    [
      "@semantic-release/release-notes-generator",
      {
        "preset": "conventionalcommits"
      }
    ],
    "@semantic-release/github"
  ]
}
```

## PR Title Validation

On pull requests, the pipeline validates that the PR title follows the [Conventional Commits](https://www.conventionalcommits.org/) format using [amannn/action-semantic-pull-request](https://github.com/amannn/action-semantic-pull-request). This is important because squash merges use the PR title as the commit message, which semantic-release uses to determine the next version.

Valid examples: `feat: add user profiles`, `fix(auth): handle expired tokens`, `feat!: redesign API`

## FAQ

### Why is `@semantic-release/npm` excluded?
The default semantic-release config includes the npm plugin, which requires a `package.json` at the root. For non-Node.js projects, this causes an `ENOPKG` error. The `.releaserc.json` must explicitly list only the plugins you need.

### How are images tagged?
On every run: `<short-sha>`. On PRs: also `pr-<number>`. On main with a new release: also `<version>` and `latest`.

### Can I use this in a monorepo?
Yes. Set `service_path` to the subdirectory and add a `tagFormat` to your `.releaserc.json` (e.g., `"tagFormat": "my-service-v${version}"`) to scope releases per service.
