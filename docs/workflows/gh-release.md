---
title: Github Release
---

<!-- action-docs-header source=".github/workflows/gh-release.yaml" -->
## Github Release
<!-- action-docs-header source=".github/workflows/gh-release.yaml" -->

## Description

This workflow creates a release based on the tag.

<!-- action-docs-inputs source=".github/workflows/gh-release.yaml" -->
### Inputs

| name | description | type | required | default |
| --- | --- | --- | --- | --- |
| `tag` | <p>The tag to release (for manual releases). If not provided, uses semantic-release for automatic versioning.</p> | `string` | `false` | `""` |
| `use_semantic_release` | <p>Use semantic-release for automatic versioning and changelog generation</p> | `boolean` | `false` | `true` |
| `update_version_aliases` | <p>Automatically update version alias tags (e.g., v1 and v1.2) to point to the latest release.</p> | `boolean` | `false` | `false` |
| `app_id` | <p>GitHub App ID (for generating a token if using GitHub App authentication)</p> | `string` | `false` | `""` |
<!-- action-docs-inputs source=".github/workflows/gh-release.yaml" -->

<!-- action-docs-outputs source=".github/workflows/gh-release.yaml" -->
### Outputs

| name | description |
| --- | --- |
| `version` | <p>The version that was released</p> |
| `new_release_published` | <p>Whether a new release was published</p> |
<!-- action-docs-outputs source=".github/workflows/gh-release.yaml" -->

<!-- action-docs-usage source=".github/workflows/gh-release.yaml" project="dnd-it/github-workflows/.github/workflows/gh-release.yaml" version="v2" -->
### Usage

```yaml
jobs:
  job1:
    uses: dnd-it/github-workflows/.github/workflows/gh-release.yaml@v2
    with:
      tag:
      # The tag to release (for manual releases). If not provided, uses semantic-release for automatic versioning.
      #
      # Type: string
      # Required: false
      # Default: ""

      use_semantic_release:
      # Use semantic-release for automatic versioning and changelog generation
      #
      # Type: boolean
      # Required: false
      # Default: true

      update_version_aliases:
      # Automatically update version alias tags (e.g., v1 and v1.2) to point to the latest release.
      #
      # Type: boolean
      # Required: false
      # Default: false

      app_id:
      # GitHub App ID (for generating a token if using GitHub App authentication)
      #
      # Type: string
      # Required: false
      # Default: ""
```
<!-- action-docs-usage source=".github/workflows/gh-release.yaml" project="dnd-it/github-workflows/.github/workflows/gh-release.yaml" version="v2" -->

# Example

# FAQ
