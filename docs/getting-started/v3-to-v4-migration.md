---
title: Migrating service-pipeline v3 → v4
---

# Migrating `service-pipeline` v3 → v4

`v4` is a breaking change. It replaces the semantic-release + ArgoCD pipeline
with [action-releaser](https://github.com/DND-IT/action-releaser) +
[action-deployer](https://github.com/DND-IT/action-deployer) and switches the
cross-job image transport from GitHub artifacts to GHCR images.

This guide lists every change a consumer needs to make to move from `@v3` to
`@v4`.

## Summary of breaking changes

| Area | v3 | v4 |
|---|---|---|
| Release | semantic-release + `.releaserc.json` | `action-releaser` + `cliff.toml` |
| Deploy | `argocd-cli.yaml` subcall | `action-deployer` inside pipeline |
| PR preview | `argocd-prepare` + `argocd-set-image` jobs | `deploy` job with `pr_environment` |
| Cross-job image transport | GitHub artifact tarball | GHCR build-cache image |
| `latest` on main | advances on every main push | advances **only** on release-producing commits |
| PR title validation | built-in (`amannn/action-semantic-pull-request`) | removed; add separately if needed |
| `tag_prefix` default | defined per repo in `.releaserc.json` | `v` (single-service) — monorepos must set `tag_prefix` per target |
| Output `new_release_published` | ✓ | renamed to `published` |
| Output `new_release_version` | ✓ | renamed to `version` |
| Output `image_pushed` | ✓ | removed |
| Output `image_tags` | ✓ | removed (use `image_sha` / `image_ref`) |
| Input `validate_pr_title` | ✓ | removed |
| Input `argocd_app_name`, `argocd_image_params` | ✓ | removed |
| Input `config_path` | required | optional |
| Input `service_path` | optional, default `.` | optional, resolved from matrix-config |
| Input `pr_environment` | — | new, defaults to `dev` |
| Input `release` | — | new; `auto` (default) or `gated` |

## Step-by-step migration

### 1. Update the `uses:` pin

```yaml
# before
uses: DND-IT/github-workflows/.github/workflows/service-pipeline.yaml@v3
# after
uses: DND-IT/github-workflows/.github/workflows/service-pipeline.yaml@v4
```

### 2. Replace `.releaserc.json` with `cliff.toml`

Delete `.releaserc.json` and add a minimal `cliff.toml` at the repo root (or
at `service_path` for monorepos):

```toml
[changelog]
header = ""
body = """
{% for group, commits in commits | group_by(attribute="group") %}
### {{ group | upper_first }}
{% for commit in commits %}
- {{ commit.message | upper_first }}
{% endfor %}
{% endfor %}
"""
trim = true

[git]
conventional_commits = true
filter_unconventional = false
commit_parsers = [
  { message = "^feat", group = "Features" },
  { message = "^fix", group = "Bug Fixes" },
]
```

See [action-releaser](https://github.com/DND-IT/action-releaser) for the full
config surface.

### 3. Preserve your existing version history

If your repo previously released under plain `v1.2.3` tags, add
`tag_prefix: v` explicitly to `matrix-config.yaml` (this is the `v4` default,
but being explicit prevents surprises):

```yaml
global:
  tag_prefix: v
```

If your repo is a **monorepo** that previously used
`tagFormat: "my-service-v${version}"`, set the target-specific prefix:

```yaml
service:
  my-service:
    tag_prefix: my-service-v
```

### 4. Remove ArgoCD inputs

Delete `argocd_app_name` and `argocd_image_params` inputs from your caller.
`action-deployer` now handles both production and PR preview deploys; the
target environment for PRs is controlled by `pr_environment` (defaults to
`dev`).

### 5. Rename outputs in downstream steps

```yaml
# before
needs.pipeline.outputs.new_release_published
needs.pipeline.outputs.new_release_version
# after
needs.pipeline.outputs.published
needs.pipeline.outputs.version
```

`image_pushed` and `image_tags` are gone. Use `image_sha` or `image_ref` if
you need the tag used to push.

### 6. Add `closed` to PR trigger types

The `cleanup` job deletes `pr-{N}*` tags from the PR environment's ECR when a
PR closes. For this to run, include `closed` in the PR trigger:

```yaml
on:
  pull_request:
    types: [opened, synchronize, reopened, closed]
```

### 7. Restore PR title validation if you need it

`v4` removed the built-in title check. If you still want one, add it as a
separate job in your caller:

```yaml
jobs:
  pr-title:
    if: github.event_name == 'pull_request'
    runs-on: ubuntu-latest
    steps:
      - uses: amannn/action-semantic-pull-request@v6
        env:
          GITHUB_TOKEN: ${{ github.token }}
```

### 8. Set up GHCR build-cache pruning

`v4` pushes every build to `ghcr.io/{owner}/{repo}/build-cache` as the
cross-job transport medium. Without a cleanup, that accumulates forever. Add
a scheduled workflow to your repo:

```yaml
name: Prune GHCR build-cache

on:
  schedule:
    - cron: '0 3 * * *'

jobs:
  prune:
    uses: DND-IT/github-workflows/.github/workflows/docker-cleanup.yaml@v4
    with:
      mode: prune-cache
      max_age_days: 14
```

### 9. Understand the release-gated contract

Under `v3`, every push to main advanced `latest` and `<short-sha>` tags in
ECR. Under `v4`, tags only advance on commits that trigger a release (feat,
fix, or anything else your `cliff.toml` mapping emits a bump for). Chore and
docs commits build but do **not** push to ECR.

If you depended on every main push advancing `latest`, you have two options:

- Adopt the release-gated contract (recommended): downstream consumers pin
  to the release tag (`1.7.3`) instead of `latest`.
- Opt out by making every commit a release: set your `cliff.toml` to emit a
  patch bump for every commit type.

### 10. (Optional) `gated` release strategy

If you want main-branch merges to open a release PR rather than publishing
immediately, set `release: gated`:

```yaml
with:
  release: gated
```

The first `feat:`/`fix:` merge creates a release PR; merging that PR
publishes the release. Non-release commits still build but neither open a
release PR nor push to ECR.

## Behavioural differences worth knowing about

### Release is published AFTER every ECR push succeeds

In `v3`, the GitHub release was created before the push step finished in
some failure paths. `v4` preserves the invariant: the release is published
only after every matrix environment's tag-push has succeeded. If `tag-push`
fails in any env, the release is **not** created.

### PR images only go to `pr_environment`

In `v3`, PR images were built but not pushed to any environment ECR. In
`v4`, PR images push to `pr_environment`'s ECR only (default `dev`) with
`pr-{N}` and `pr-{N}-{sha}` tags, and are deleted on PR close.

### `tag_prefix` default changed

In `v3`, your `.releaserc.json` defined `tagFormat`. In `v4`, the default is
`v` (producing `v1.7.3`). Monorepo consumers must set `tag_prefix` in
`matrix-config.yaml` per target.
