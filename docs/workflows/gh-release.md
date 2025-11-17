---
title: Github Release
---

<!-- action-docs-header source=".github/workflows/gh-release.yaml" -->
## Github Semantic Release [Alpha]
<!-- action-docs-header source=".github/workflows/gh-release.yaml" -->

## Description

This workflow creates a release based on the tag.

<!-- action-docs-inputs source=".github/workflows/gh-release.yaml" -->
### Inputs

| name | description | type | required | default |
| --- | --- | --- | --- | --- |
| `tag` | <p>The tag to release (for manual releases). If not provided, uses semantic-release for automatic versioning.</p> | `string` | `false` | `""` |
| `tag_format` | <p>The format of the tag to release (for manual releases).</p> | `string` | `false` | `v${version}` |
| `use_semantic_release` | <p>Use semantic-release for automatic versioning and changelog generation</p> | `boolean` | `false` | `true` |
| `update_version_aliases` | <p>Automatically update version alias tags (e.g., v1 and v1.2) to point to the latest release.</p> | `boolean` | `false` | `false` |
| `dry_run` | <p>Run in dry-run mode to preview the release without creating it.</p> | `boolean` | `false` | `false` |
| `app_id` | <p>GitHub App ID (for generating a token if using GitHub App authentication)</p> | `string` | `false` | `""` |
<!-- action-docs-inputs source=".github/workflows/gh-release.yaml" -->

<!-- action-docs-outputs source=".github/workflows/gh-release.yaml" -->
### Outputs

| name | description |
| --- | --- |
| `new_release_published` | <p>Whether a new release was published (true or false)</p> |
| `new_release_version` | <p>Version of the new release (e.g. 1.3.0)</p> |
| `new_release_major_version` | <p>Major version of the new release (e.g. 1)</p> |
| `new_release_minor_version` | <p>Minor version of the new release (e.g. 3)</p> |
| `new_release_patch_version` | <p>Patch version of the new release (e.g. 0)</p> |
| `new_release_git_tag` | <p>The Git tag associated with the new release (e.g. v1.3.0)</p> |
| `new_release_git_head` | <p>The sha of the last commit being part of the new release</p> |
| `dry_run` | <p>Whether this was a dry-run (true) or actual release (false)</p> |
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

      tag_format:
      # The format of the tag to release (for manual releases).
      #
      # Type: string
      # Required: false
      # Default: v${version}

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

      dry_run:
      # Run in dry-run mode to preview the release without creating it.
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
