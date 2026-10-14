---
title: Github Release
---

<!-- action-docs-header source=".github/workflows/gh-release.yaml" -->
## GitHub Release (git-cliff)
<!-- action-docs-header source=".github/workflows/gh-release.yaml" -->

## Description

This workflow creates a release based on the tag.

<!-- action-docs-inputs source=".github/workflows/gh-release.yaml" -->
### Inputs

| name | description | type | required | default |
| --- | --- | --- | --- | --- |
| `service_name` | <p>Name of the service (used for scoped tag prefix, e.g., 'titan-api'). Leave empty for whole-repo releases.</p> | `string` | `false` | `""` |
| `service_path` | <p>Path to the service directory for monorepo filtering (e.g., 'services/titan-api'). Only commits touching this path trigger releases.</p> | `string` | `false` | `""` |
| `cliff_config` | <p>Path to git-cliff configuration file. If not found, uses an embedded default.</p> | `string` | `false` | `cliff.toml` |
| `update_version_aliases` | <p>Automatically update version alias tags (e.g., v1 and v1.2) to point to the latest release.</p> | `boolean` | `false` | `false` |
| `dry_run` | <p>Run in dry-run mode to preview the release without creating it.</p> | `boolean` | `false` | `false` |
| `metadata_file` | <p>File path containing extra metadata to append to the release version (e.g., build info). Empty to skip.</p> | `string` | `false` | `""` |
| `app_id` | <p>GitHub App ID for authentication</p> | `string` | `false` | `""` |
<!-- action-docs-inputs source=".github/workflows/gh-release.yaml" -->

<!-- action-docs-outputs source=".github/workflows/gh-release.yaml" -->
### Outputs

| name | description |
| --- | --- |
| `new_release_published` | <p>Whether a new release was published ('true' or 'false')</p> |
| `new_release_version` | <p>Version of the new release (e.g. 1.3.0)</p> |
| `new_release_major_version` | <p>Major version of the new release (e.g. 1)</p> |
| `new_release_minor_version` | <p>Minor version of the new release (e.g. 3)</p> |
| `new_release_patch_version` | <p>Patch version of the new release (e.g. 0)</p> |
| `new_release_git_tag` | <p>The Git tag associated with the new release</p> |
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
      service_name:
      # Name of the service (used for scoped tag prefix, e.g., 'titan-api'). Leave empty for whole-repo releases.
      #
      # Type: string
      # Required: false
      # Default: ""

      service_path:
      # Path to the service directory for monorepo filtering (e.g., 'services/titan-api'). Only commits touching this path trigger releases.
      #
      # Type: string
      # Required: false
      # Default: ""

      cliff_config:
      # Path to git-cliff configuration file. If not found, uses an embedded default.
      #
      # Type: string
      # Required: false
      # Default: cliff.toml

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

      metadata_file:
      # File path containing extra metadata to append to the release version (e.g., build info). Empty to skip.
      #
      # Type: string
      # Required: false
      # Default: ""

      app_id:
      # GitHub App ID for authentication
      #
      # Type: string
      # Required: false
      # Default: ""
```
<!-- action-docs-usage source=".github/workflows/gh-release.yaml" project="dnd-it/github-workflows/.github/workflows/gh-release.yaml" version="v2" -->

# Examples

## Basic Release

```yaml
jobs:
  release:
    uses: dnd-it/github-workflows/.github/workflows/gh-release.yaml@v3
    with:
      use_semantic_release: true
      update_version_aliases: true
```

This will create a release using semantic-release with conventional commits and update version alias tags (e.g., `v1`, `v1.2`).

## Monorepo / Subdirectory Releases

For monorepo setups where you want to release individual packages or components with separate versioning, use the `working_directory` input:

```yaml
jobs:
  release-lambda:
    uses: dnd-it/github-workflows/.github/workflows/gh-release.yaml@v3
    with:
      working_directory: packages/lambda
      use_semantic_release: true
```

### Subdirectory Configuration

Create a `.releaserc.json` file in your subdirectory (e.g., `packages/lambda/.releaserc.json`) with a custom `tagFormat`:

```json
{
  "branches": [
    "main"
  ],
  "tagFormat": "lambda-v${version}",
  "plugins": [
    [
      "@semantic-release/commit-analyzer",
      {
        "preset": "conventionalcommits",
        "releaseRules": [
          { "type": "feat", "release": "minor" },
          { "type": "fix", "release": "patch" },
          { "type": "perf", "release": "patch" },
          { "type": "revert", "release": "patch" }
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

**Key points:**

1. **Custom Tag Format**: Use a unique `tagFormat` (e.g., `lambda-v${version}`) to avoid conflicts with main repo tags
2. **No Changelog/Git Plugins**: Omit `@semantic-release/changelog` and `@semantic-release/git` plugins to avoid conflicts. Let the main repository handle the changelog.
3. **GitHub Releases Only**: Subdirectory releases create GitHub releases with proper release notes but don't commit back to the repo

### Multiple Packages Example

```yaml
jobs:
  release-api:
    uses: dnd-it/github-workflows/.github/workflows/gh-release.yaml@v3
    with:
      working_directory: packages/api
      use_semantic_release: true

  release-frontend:
    uses: dnd-it/github-workflows/.github/workflows/gh-release.yaml@v3
    with:
      working_directory: packages/frontend
      use_semantic_release: true
```

Each package will have its own:
- Version numbering (e.g., `api-v1.2.0`, `frontend-v2.1.0`)
- GitHub release with generated release notes
- Independent release cadence

## Manual Release

```yaml
jobs:
  release:
    uses: dnd-it/github-workflows/.github/workflows/gh-release.yaml@v3
    with:
      use_semantic_release: false
      tag: v1.0.0
```

## Custom Tag Format (Override)

You can override the `tagFormat` from `.releaserc.json` using the workflow input:

```yaml
jobs:
  release:
    uses: dnd-it/github-workflows/.github/workflows/gh-release.yaml@v3
    with:
      tag_format: "release-v${version}"
      use_semantic_release: true
```

**Note**: If you don't provide `tag_format` as a workflow input, the workflow will use the `tagFormat` defined in your `.releaserc.json` file.

# FAQ

## How does `working_directory` work?

The `working_directory` input tells semantic-release to run from a specific subdirectory. Semantic-release will:
- Look for `.releaserc.json` in that directory
- Use paths relative to that directory
- Analyze all repository commits (not filtered by directory)

## Why remove changelog and git plugins from subdirectory configs?

When multiple releases write to the same repository, having multiple semantic-release instances commit changes can cause conflicts. Best practice:
- **Main repo**: Uses `@semantic-release/changelog` and `@semantic-release/git` to maintain `/CHANGELOG.md`
- **Subdirectories**: Only use `@semantic-release/github` to create releases

## Can I filter commits by directory for subdirectory releases?

Semantic-release doesn't have built-in path filtering. All commits in the repository history will be analyzed for version bumps and included in release notes. Consider using:
- **Commit scopes**: Use conventional commit scopes (e.g., `feat(api):`, `fix(frontend):`) to organize release notes
- **Monorepo plugins**: Third-party plugins like `semantic-release-monorepo` can filter by path, but add complexity

## What happens on the first subdirectory release?

The first release in a subdirectory will:
- Start at version `1.0.0` (since no tags with that `tagFormat` exist)
- Include all repository commits in the release notes
- Create a GitHub release with tag like `mypackage-v1.0.0`

Subsequent releases will only include commits since the last release with that tag format.
