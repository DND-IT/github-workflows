---
title: Update Helm Image Tag in Values.yaml
---

## Description

Simple workflow to update the image tag in a files. It creates a pull request with the changes.

<!-- action-docs-inputs source=".github/workflows/gitops-image-tag.yaml" -->
### Inputs

| name | description | type | required | default |
| --- | --- | --- | --- | --- |
| `image_tag` | <p>The tag of the Docker image</p> | `string` | `true` | `""` |
| `image_tag_key` | <p>Key in the values file to update (e.g., image.tag)</p> | `string` | `false` | `image_tag` |
| `values_file` | <p>Path to the Helm values file</p> | `string` | `false` | `deploy/app/values-common.yaml` |
| `create_pr` | <p>Whether to create a pull request</p> | `boolean` | `false` | `true` |
| `target_branch` | <p>The target branch for the pull request. Defaults the default branch of the repository.</p> | `string` | `false` | `""` |
<!-- action-docs-inputs source=".github/workflows/gitops-image-tag.yaml" -->

<!-- action-docs-outputs source=".github/workflows/gitops-image-tag.yaml" -->

<!-- action-docs-outputs source=".github/workflows/gitops-image-tag.yaml" -->

<!-- action-docs-usage source=".github/workflows/gitops-image-tag.yaml" project="dnd-it/github-workflows/.github/workflows/gitops-image-tag.yaml" version="v2" -->
### Usage

```yaml
jobs:
  job1:
    uses: dnd-it/github-workflows/.github/workflows/gitops-image-tag.yaml@v2
    with:
      image_tag:
      # The tag of the Docker image
      #
      # Type: string
      # Required: true
      # Default: ""

      image_tag_key:
      # Key in the values file to update (e.g., image.tag)
      #
      # Type: string
      # Required: false
      # Default: image_tag

      values_file:
      # Path to the Helm values file
      #
      # Type: string
      # Required: false
      # Default: deploy/app/values-common.yaml

      create_pr:
      # Whether to create a pull request
      #
      # Type: boolean
      # Required: false
      # Default: true

      target_branch:
      # The target branch for the pull request. Defaults the default branch of the repository.
      #
      # Type: string
      # Required: false
      # Default: ""
```
<!-- action-docs-usage source=".github/workflows/gitops-image-tag.yaml" project="dnd-it/github-workflows/.github/workflows/gitops-image-tag.yaml" version="v2" -->

## Example

```yaml
name: Update Image Tag
on:
  workflow_run:
    workflows: ["Build and Push Docker Image"] # Your workflow name for the docker build
    types:
      - completed

permissions:
  contents: write
  pull-requests: write

jobs:
  job1:
    uses: dnd-it/github-workflows/.github/workflows/gitops-image-tag.yaml@v2
    with:
      image_tag: ${{ github.sha }}
      values_file: "deploy/app/envs/prod/values-common.yaml"
      create_pr: true

```

This example updates the `image_tag` key in the `deploy/app/values-common.yaml` file to `v1.0.0` and creates a pull request with the changes.

## FAQ

**Q: How can I update multiple values files?**

A: Not possible at the moment, PRs are welcome.
