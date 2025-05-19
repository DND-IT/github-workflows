---
title: Helm Diff Preview
---

## Description

This GitHub Action generates a diff of Helm chart templates between the current branch and the base branch of a pull request. It uses the `helm template` command to render the templates and compares them using `diff`. The action is designed to be used in a GitHub Actions workflow, particularly for pull requests.

<!-- action-docs-inputs source=".github/workflows/gitops-helm-diff.yaml" -->
### Inputs

| name | description | type | required | default |
| --- | --- | --- | --- | --- |
| `helm_chart_path` | <p>Path to the Helm chart directory</p> | `string` | `false` | `deploy/app` |
| `common_values_path` | <p>Path to the common values.yaml file</p> | `string` | `false` | `deploy/app/values.yaml` |
| `environments_path` | <p>Path to the directory containing environment-specific values</p> | `string` | `false` | `deploy/app/envs` |
| `output_path` | <p>Path to the output directory for diffs</p> | `string` | `false` | `output` |
| `base_branch` | <p>Base branch for comparison</p> | `string` | `false` | `${{ github.event.pull_request.base.ref }}` |
| `helm_release_name` | <p>Name to use for the Helm release when templating</p> | `string` | `false` | `release-name` |
| `helm_repo_url` | <p>URL of the Helm repository to add</p> | `string` | `false` | `https://dnd-it.github.io/helm-charts` |
| `helm_repo_name` | <p>Name to give to the Helm repository</p> | `string` | `false` | `dnd-it` |
| `additional_helm_flags` | <p>Additional flags to pass to helm template command</p> | `string` | `false` | `""` |
| `debug` | <p>Enable debug output</p> | `string` | `false` | `false` |
<!-- action-docs-inputs source=".github/workflows/gitops-helm-diff.yaml" -->

<!-- action-docs-outputs source=".github/workflows/gitops-helm-diff.yaml" -->

<!-- action-docs-outputs source=".github/workflows/gitops-helm-diff.yaml" -->

<!-- action-docs-usage source=".github/workflows/gitops-helm-diff.yaml" project="dnd-it/github-workflows/.github/workflows/gitops-helm-diff.yaml" version="v2" -->
### Usage

```yaml
jobs:
  job1:
    uses: dnd-it/github-workflows/.github/workflows/gitops-helm-diff.yaml@v2
    with:
      helm_chart_path:
      # Path to the Helm chart directory
      #
      # Type: string
      # Required: false
      # Default: deploy/app

      common_values_path:
      # Path to the common values.yaml file
      #
      # Type: string
      # Required: false
      # Default: deploy/app/values.yaml

      environments_path:
      # Path to the directory containing environment-specific values
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

      helm_release_name:
      # Name to use for the Helm release when templating
      #
      # Type: string
      # Required: false
      # Default: release-name

      helm_repo_url:
      # URL of the Helm repository to add
      #
      # Type: string
      # Required: false
      # Default: https://dnd-it.github.io/helm-charts

      helm_repo_name:
      # Name to give to the Helm repository
      #
      # Type: string
      # Required: false
      # Default: dnd-it

      additional_helm_flags:
      # Additional flags to pass to helm template command
      #
      # Type: string
      # Required: false
      # Default: ""

      debug:
      # Enable debug output
      #
      # Type: string
      # Required: false
      # Default: false
```
<!-- action-docs-usage source=".github/workflows/gitops-helm-diff.yaml" project="dnd-it/github-workflows/.github/workflows/gitops-helm-diff.yaml" version="v2" -->

## Example

```yaml
name: Helm Diff Example

on:
  pull_request:
    branches:
      - main
    paths:
      - deploy/app/**

jobs:
  test_tf_feature:
    uses: ./.github/workflows/gitops-helm-diff.yaml
    with:
      debug: true

## FAQ


