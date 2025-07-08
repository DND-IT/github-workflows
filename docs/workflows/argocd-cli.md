---
title: ArgoCD CLI
---

## Description

<!-- action-docs-inputs source=".github/workflows/argocd-cli.yaml" -->
### Inputs

| name | description | type | required | default |
| --- | --- | --- | --- | --- |
| `argocd_version` | <p>ArgoCD CLI version to use</p> | `string` | `false` | `""` |
| `argocd_architecture` | <p>Architecture for ArgoCD CLI (default is amd64)</p> | `string` | `false` | `amd64` |
| `argocd_server` | <p>ArgoCD server URL</p> | `string` | `false` | `""` |
| `argocd_grpc_web` | <p>Use gRPC-web for ArgoCD CLI</p> | `string` | `false` | `false` |
| `argocd_commands` | <p>ArgoCD CLI commands to run. Can be a single command or multiple commands separated by newlines. Example: |   app list   app get my-app   app sync my-app --prune</p> | `string` | `true` | `""` |
| `pre_run` | <p>Custom commands to run before ArgoCD commands</p> | `string` | `false` | `""` |
| `post_run` | <p>Custom commands to run after ArgoCD commands</p> | `string` | `false` | `""` |
| `working_directory` | <p>Working directory for running commands</p> | `string` | `false` | `.` |
| `runner` | <p>GitHub runner to use</p> | `string` | `false` | `ubuntu-latest` |
<!-- action-docs-inputs source=".github/workflows/argocd-cli.yaml" -->

<!-- action-docs-outputs source=".github/workflows/argocd-cli.yaml" -->

<!-- action-docs-outputs source=".github/workflows/argocd-cli.yaml" -->

<!-- action-docs-usage source=".github/workflows/argocd-cli.yaml" project="dnd-it/github-workflows/.github/workflows/argocd-cli.yaml" version="v2" -->
### Usage

```yaml
jobs:
  job1:
    uses: dnd-it/github-workflows/.github/workflows/argocd-cli.yaml@v2
    with:
      argocd_version:
      # ArgoCD CLI version to use
      #
      # Type: string
      # Required: false
      # Default: ""

      argocd_architecture:
      # Architecture for ArgoCD CLI (default is amd64)
      #
      # Type: string
      # Required: false
      # Default: amd64

      argocd_server:
      # ArgoCD server URL
      #
      # Type: string
      # Required: false
      # Default: ""

      argocd_grpc_web:
      # Use gRPC-web for ArgoCD CLI
      #
      # Type: string
      # Required: false
      # Default: false

      argocd_commands:
      # ArgoCD CLI commands to run. Can be a single command or multiple commands separated by newlines.
      # Example: |
      #   app list
      #   app get my-app
      #   app sync my-app --prune
      #
      # Type: string
      # Required: true
      # Default: ""

      pre_run:
      # Custom commands to run before ArgoCD commands
      #
      # Type: string
      # Required: false
      # Default: ""

      post_run:
      # Custom commands to run after ArgoCD commands
      #
      # Type: string
      # Required: false
      # Default: ""

      working_directory:
      # Working directory for running commands
      #
      # Type: string
      # Required: false
      # Default: .

      runner:
      # GitHub runner to use
      #
      # Type: string
      # Required: false
      # Default: ubuntu-latest
```
<!-- action-docs-usage source=".github/workflows/argocd-cli.yaml" project="dnd-it/github-workflows/.github/workflows/argocd-cli.yaml" version="v2" -->

## Example

### Basic Usage

```yaml
jobs:
  argocd-commands:
    uses: dnd-it/github-workflows/.github/workflows/argocd-cli.yaml@v2
    with:
      argocd_commands: |
        version --client
        app list
        app get my-app
```

### With Server Connection

```yaml
jobs:
  sync-application:
    uses: dnd-it/github-workflows/.github/workflows/argocd-cli.yaml@v2
    with:
      argocd_server: "argocd.example.com"
      argocd_grpc_web: "true"
      argocd_commands: |
        app sync my-app --prune
        app wait my-app --health
    secrets:
      argocd_auth_token: ${{ secrets.ARGOCD_AUTH_TOKEN }}
```

### With Pre/Post Commands

```yaml
jobs:
  deploy-with-setup:
    uses: dnd-it/github-workflows/.github/workflows/argocd-cli.yaml@v2
    with:
      pre_run: |
        echo "Setting up environment..."
        export DEPLOY_ENV=production
      argocd_commands: |
        app create my-app --repo https://github.com/org/repo --path k8s --dest-server https://kubernetes.default.svc
        app sync my-app
      post_run: |
        echo "Deployment completed"
        curl -X POST https://webhook.site/deployment-complete
```

### Using Specific Version

```yaml
jobs:
  argocd-v2-12:
    uses: dnd-it/github-workflows/.github/workflows/argocd-cli.yaml@v2
    with:
      argocd_version: "3.0.1"
      argocd_architecture: "amd64"
      argocd_commands: |
        version --client
        repo list
```

## FAQ

### Q: How do I authenticate with an ArgoCD server?

A: Use the `argocd_server` input to specify your server URL and pass the authentication token as a secret:

```yaml
with:
  argocd_server: "argocd.example.com"
secrets:
  argocd_auth_token: ${{ secrets.ARGOCD_TOKEN }}
```

### Q: Can I use environment variables from GitHub?

A: Yes, the workflow supports GitHub environment variables. If you don't provide an input, it will fall back to the corresponding GitHub variable (e.g., `vars.argocd_version`).

### Q: How do I run multiple ArgoCD commands?

A: Use the multiline YAML syntax with the pipe (`|`) character:

```yaml
argocd_commands: |
  app list
  app get my-app
  app sync my-app --prune
```

### Q: What architectures are supported?

A: The workflow supports both `amd64` (default) and `arm64` architectures. Specify using the `argocd_architecture` input.

### Q: Can I use this workflow with a custom runner?

A: Yes, use the `runner` input to specify a custom runner:

```yaml
with:
  runner: "self-hosted"
  argocd_commands: "version --client"
```

### Q: How do I handle errors in commands?

A: The workflow uses `set -e` which will stop execution on the first error. If you need to handle errors gracefully, use shell error handling in your commands:

```yaml
argocd_commands: |
  app sync my-app || echo "Sync failed, but continuing..."
  app list
```
