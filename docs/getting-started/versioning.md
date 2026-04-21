---
title: Versioning & pinning
---

# Versioning & pinning

This repo emits **two kinds of release tags** on every main-branch merge, both
driven by [action-releaser](https://github.com/DND-IT/action-releaser) and
scoped by conventional-commit messages.

## Global release tags

Tag format: `v<major>.<minor>.<patch>` (e.g. `v4.2.0`).

Produced on every release-worthy commit to main, regardless of which files
changed. Floating aliases `v<major>` and `v<major>.<minor>` are updated by
the release pipeline.

**Pin against the global tag when you want a consistent bundle of all
reusable workflows at the same version:**

```yaml
uses: DND-IT/github-workflows/.github/workflows/service-pipeline.yaml@v4
```

This is the default and what most consumers should use.

## Per-workflow release tags

Tag format: `<workflow-name>-v<major>.<minor>.<patch>`
(e.g. `service-pipeline-v1.0.0`, `docker-build-v2.3.1`).

Produced whenever a main-branch commit touches that specific workflow file.
A commit that edits only `service-pipeline.yaml` bumps
`service-pipeline-v*` and the global `v*`, but does **not** bump any other
per-workflow tag.

**Pin against a per-workflow tag when you want to isolate your repo from
changes to unrelated workflows:**

```yaml
uses: DND-IT/github-workflows/.github/workflows/service-pipeline.yaml@service-pipeline-v1.0.0
```

This is useful when you want to upgrade `service-pipeline` without also
upgrading every other workflow's behaviour.

## Which tag is right for me?

| You want to ... | Pin against |
|---|---|
| Follow the whole repo at a known-good point | `@v4` |
| Upgrade a single workflow in isolation | `@<workflow>-v<ver>` |
| Track the bleeding edge | `@main` (not recommended for prod) |

## How releases are triggered

- `feat:` commit → minor bump (global + every touched per-workflow tag)
- `fix:` commit → patch bump
- `feat!:` / `BREAKING CHANGE:` → major bump
- `chore:` / `docs:` / `refactor:` without `!` → no release

The release commit analyzer is configured in `cliff.toml` at the repo root.

## When a commit touches multiple workflows

A single commit that edits `docker-build.yaml` and `docker-push.yaml`
produces three tags on that run:

- `docker-build-v<next>` (bumped because docker-build.yaml changed)
- `docker-push-v<next>` (bumped because docker-push.yaml changed)
- `v<next>` (global, bumped because anything release-worthy changed)

Unaffected workflow tags (e.g. `tf-plan-v*`) are not touched.
