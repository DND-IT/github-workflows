# Versioning

## Overview

This repository uses [git-cliff](https://git-cliff.org/) for automated versioning based on [conventional commits](https://www.conventionalcommits.org/). Releases are created automatically when changes are pushed to the `main` branch.

## Tag Format

### Global releases (this repo)

Tags follow standard semver: `v{major}.{minor}.{patch}` (e.g., `v4.0.0`).

Version aliases are automatically updated:
- `v{major}` (e.g., `v4`) — always points to the latest release in that major version
- `v{major}.{minor}` (e.g., `v4.0`) — always points to the latest patch in that minor version

### Scoped releases (caller repos)

For monorepos or repos with multiple services, tags include a service prefix: `{service_name}-v{major}.{minor}.{patch}` (e.g., `titan-api-v1.3.0`).

Scoped version aliases:
- `{service_name}-v{major}` (e.g., `titan-api-v1`)
- `{service_name}-v{major}.{minor}` (e.g., `titan-api-v1.3`)

git-cliff uses `--tag-pattern` and `--include-path` to only consider commits relevant to the specific service.

## Conventional Commits

Version bumps are determined by commit prefixes:

| Prefix | Version Bump | Example |
|--------|-------------|---------|
| `feat!:` | Major | `feat!: redesign API endpoints` |
| `feat:` | Minor | `feat: add new workflow input` |
| `fix:` | Patch | `fix: correct tag format` |

Other prefixes (`chore:`, `docs:`, `ci:`, `refactor:`, `test:`, `perf:`, `style:`) do not trigger releases on their own but are included in changelogs.

## Using `gh-release.yaml`

### Basic usage (whole repo)

```yaml
jobs:
  release:
    uses: DND-IT/github-workflows/.github/workflows/gh-release.yaml@v4
    with:
      update_version_aliases: true
      app_id: ${{ vars.APP_ID }}
    secrets:
      app_private_key: ${{ secrets.APP_PRIVATE_KEY }}
```

### Scoped usage (monorepo service)

```yaml
jobs:
  release:
    uses: DND-IT/github-workflows/.github/workflows/gh-release.yaml@v4
    with:
      service_name: titan-api
      service_path: services/titan-api
      update_version_aliases: true
      app_id: ${{ vars.APP_ID }}
    secrets:
      app_private_key: ${{ secrets.APP_PRIVATE_KEY }}
```

### Inputs

| Input | Required | Default | Description |
|-------|----------|---------|-------------|
| `service_name` | No | `''` | Service name for scoped tag prefix. Leave empty for whole-repo releases. |
| `service_path` | No | `''` | Path to service directory for monorepo filtering. |
| `cliff_config` | No | `cliff.toml` | Path to git-cliff config. Uses embedded default if not found. |
| `update_version_aliases` | No | `false` | Auto-update major/minor alias tags. |
| `dry_run` | No | `false` | Preview release without creating it. |
| `metadata_file` | No | `''` | File with metadata to append to version (e.g., build info). |
| `app_id` | No | — | GitHub App ID for authentication. |

### Outputs

| Output | Description |
|--------|-------------|
| `new_release_published` | `'true'` or `'false'` |
| `new_release_version` | Version string (e.g., `1.3.0`) |
| `new_release_major_version` | Major version number |
| `new_release_minor_version` | Minor version number |
| `new_release_patch_version` | Patch version number |
| `new_release_git_tag` | Full git tag (e.g., `v1.3.0` or `titan-api-v1.3.0`) |
| `new_release_git_head` | SHA of the release commit |
| `dry_run` | Whether this was a dry-run |

## Custom git-cliff Configuration

The workflow uses an embedded default configuration if no `cliff.toml` is found at the specified path. To customize changelog generation, create a `cliff.toml` in your repository root. See [git-cliff documentation](https://git-cliff.org/docs/configuration) for options.

---

## Migration Guide: v3 (semantic-release) → v4 (git-cliff)

### What changed

- **Release engine**: `cycjimmy/semantic-release-action` replaced by `orhun/git-cliff-action`
- **Scoped tags**: Native support via `service_name` + `service_path` inputs
- **Configuration**: `.releaserc.json` replaced by `cliff.toml` (optional — embedded default works)
- **Node.js dependency**: Removed — git-cliff is a standalone Rust binary

### Before (v3)

```yaml
jobs:
  release:
    uses: DND-IT/github-workflows/.github/workflows/gh-release.yaml@v3
    with:
      use_semantic_release: true
      tag_format: "v${version}"
      update_version_aliases: true
      app_id: ${{ vars.APP_ID }}
    secrets:
      app_private_key: ${{ secrets.APP_PRIVATE_KEY }}
```

### After (v4)

```yaml
jobs:
  release:
    uses: DND-IT/github-workflows/.github/workflows/gh-release.yaml@v4
    with:
      update_version_aliases: true
      app_id: ${{ vars.APP_ID }}
    secrets:
      app_private_key: ${{ secrets.APP_PRIVATE_KEY }}
```

### Input mapping

| v3 Input | v4 Equivalent | Notes |
|----------|--------------|-------|
| `use_semantic_release` | *(removed)* | git-cliff is always used |
| `tag_format` | *(removed)* | Determined by `service_name` presence |
| `tag` | *(removed)* | Manual tagging not supported; use `gh release create` directly |
| `working_directory` | `service_path` | Same purpose, renamed for clarity |
| `update_version_aliases` | `update_version_aliases` | Unchanged |
| `dry_run` | `dry_run` | Unchanged |
| `app_id` | `app_id` | Unchanged |
| *(new)* | `service_name` | Enables scoped tag prefix |
| *(new)* | `cliff_config` | Custom git-cliff configuration |
| *(new)* | `metadata_file` | Ported from `gh-release-on-main.yaml` |

### For `gh-release-on-main.yaml` callers

`gh-release-on-main.yaml` has been consolidated into `gh-release.yaml`. If you were using it:

**Before:**
```yaml
uses: DND-IT/github-workflows/.github/workflows/gh-release-on-main.yaml@v3
with:
  metadata_file: "VERSION_METADATA"
  update_version_aliases: true
```

**After:**
```yaml
uses: DND-IT/github-workflows/.github/workflows/gh-release.yaml@v4
with:
  metadata_file: "VERSION_METADATA"
  update_version_aliases: true
```

### For `service-pipeline.yaml` callers

No changes needed — `service-pipeline.yaml` uses internal self-references and automatically uses the new git-cliff release workflow.
