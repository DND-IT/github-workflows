---
title: Kustomize Diff Preview
---

## Description

This workflow generates a diff preview for Kustomize overlays in a GitOps setup. It compares the current state of the Kustomize overlays with the base branch and outputs the differences.

The action is designed to be used in a GitHub Actions workflow, particularly for pull requests.

It uses the `kustomize build` command to render the overlays and compares them using `diff`.

<!-- action-docs-inputs source=".github/workflows/gitops-kustomize-diff.yaml" -->
### Inputs

| name | description | type | required | default |
| --- | --- | --- | --- | --- |
| `kustomize_path` | <p>Path to the root Kustomize directory. Its assumed that base directory is nested under this path.</p> | `string` | `false` | `deploy/app` |
| `environments_path` | <p>Path to the directory containing environment-specific overlays</p> | `string` | `false` | `deploy/app/envs` |
| `output_path` | <p>Path to the output directory for diffs</p> | `string` | `false` | `output` |
| `base_branch` | <p>Base branch for comparison</p> | `string` | `false` | `${{ github.event.pull_request.base.ref }}` |
| `kustomize_args` | <p>Additional arguments to pass to kustomize build command</p> | `string` | `false` | `--enable-helm --load-restrictor LoadRestrictionsNone` |
| `debug` | <p>Enable debug output</p> | `string` | `false` | `false` |
<!-- action-docs-inputs source=".github/workflows/gitops-kustomize-diff.yaml" -->

<!-- action-docs-outputs source=".github/workflows/gitops-kustomize-diff.yaml" -->

<!-- action-docs-outputs source=".github/workflows/gitops-kustomize-diff.yaml" -->

<!-- action-docs-usage source=".github/workflows/gitops-kustomize-diff.yaml" project="dnd-it/github-workflows/.github/workflows/gitops-kustomize-diff.yaml" version="v2" -->
### Usage

```yaml
jobs:
  job1:
    uses: dnd-it/github-workflows/.github/workflows/gitops-kustomize-diff.yaml@v2
    with:
      kustomize_path:
      # Path to the root Kustomize directory. Its assumed that base directory is nested under this path.
      #
      # Type: string
      # Required: false
      # Default: deploy/app

      environments_path:
      # Path to the directory containing environment-specific overlays
      #
      # Type: string
      # Required: false
      # Default: deploy/app/envs

      output_path:
      # Path to the output directory for diffs
      #
      # Type: string
      # Required: false
      # Default: output

      base_branch:
      # Base branch for comparison
      #
      # Type: string
      # Required: false
      # Default: ${{ github.event.pull_request.base.ref }}

      kustomize_args:
      # Additional arguments to pass to kustomize build command
      #
      # Type: string
      # Required: false
      # Default: --enable-helm --load-restrictor LoadRestrictionsNone

      debug:
      # Enable debug output
      #
      # Type: string
      # Required: false
      # Default: false
```
<!-- action-docs-usage source=".github/workflows/gitops-kustomize-diff.yaml" project="dnd-it/github-workflows/.github/workflows/gitops-kustomize-diff.yaml" version="v2" -->

## Example

```yaml
name: ArgoCD Diff

on:
  pull_request:
    branches:
      - main
    paths:
      - configs/argocd/hub/**

jobs:
  kustomize-diff:
    uses: dnd-it/github-workflows/.github/workflows/gitops-kustomize-diff.yaml@v2
    with:
      kustomize_path: configs/argocd/hub
      environments_path: configs/argocd/hub
      debug: true
```

## FAQ
