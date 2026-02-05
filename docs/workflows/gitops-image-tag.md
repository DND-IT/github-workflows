---
title: GitOps Image Tag
---

## Description

Updates image tags in Helm values files and optionally creates a pull request. Supports two modes:

- **Image name search** (`image_name`) — Automatically finds all image blocks (objects with `repository` and `tag` fields) where the repository ends with the given name, and updates their tags. This is the recommended approach as it requires no maintenance when adding new image references (e.g., cronjobs).
- **Explicit keys** (`image_tag_keys`) — Updates specific YAML keys by dot-notation path. Use this when you need precise control over which fields are updated.

Both modes use `yq` to locate the exact line number, then `sed` to replace only that line, preserving the original file formatting.

<!-- action-docs-inputs source=".github/workflows/gitops-image-tag.yaml" -->
### Inputs

| name | description | type | required | default |
| --- | --- | --- | --- | --- |
| `image_tag` | <p>The tag of the Docker image</p> | `string` | `true` | `""` |
| `image_tag_keys` | <p>Newline-separated list of keys to update (e.g., webapp.image.tag). Ignored when image_name is set.</p> | `string` | `false` | `""` |
| `image_name` | <p>Image name to search for (e.g., social-media). Finds all image blocks where the repository ends with this name and updates their tag. Takes precedence over image<em>tag</em>keys.</p> | `string` | `false` | `""` |
| `values_files` | <p>Newline-separated list of file paths to update</p> | `string` | `true` | `""` |
| `create_pr` | <p>Create a pull request. If false, the changes will be committed directly to the target branch. Github Actions must have write permissions to the repository. If branch protection is enabled a Github App is required and is able to bypass branch protection rules.</p> | `boolean` | `false` | `true` |
| `pr_message` | <p>Custom message for the pull request. Defaults to a standard message.</p> | `string` | `false` | `This PR updates the Helm values files to use the latest image tag.` |
| `auto_merge` | <p>Enable auto-merge for the pull request. Only works if create_pr is true.</p> | `boolean` | `false` | `false` |
| `branch_name_prefix` | <p>Prefix for the branch name.</p> | `string` | `false` | `helm-values` |
| `target_branch` | <p>The target branch for the pull request. Defaults the default branch of the repository.</p> | `string` | `false` | `${{ github.event.repository.default_branch }}` |
| `app_id` | <p>GitHub App ID for generating a token. Required if using GitHub App authentication.</p> | `string` | `false` | `""` |
<!-- action-docs-inputs source=".github/workflows/gitops-image-tag.yaml" -->

<!-- action-docs-outputs source=".github/workflows/gitops-image-tag.yaml" -->

<!-- action-docs-outputs source=".github/workflows/gitops-image-tag.yaml" -->

## Examples

### Image name search (recommended)

Automatically finds and updates all image tags matching the given name across base and environment-specific values files. The `image_name` uses a regex match against the `repository` field — it matches any repository ending with the given name.

```yaml
jobs:
  update-image:
    uses: DND-IT/github-workflows/.github/workflows/gitops-image-tag.yaml@v3
    with:
      image_tag: "1.2.0"
      image_name: social-media
      values_files: |
        deploy/app/values.yaml
        deploy/app/envs/dev/values.yaml
        deploy/app/envs/prod/values.yaml
      create_pr: true
      auto_merge: true
      branch_name_prefix: helm/social-media
      app_id: ${{ vars.GH_APP_ID }}
    secrets:
      app_private_key: ${{ secrets.GH_APP_PRIVATE_KEY }}
```

Given a values file like:

```yaml
generic:
  image:
    repository: social-media
    tag: "1.0.0"          # <-- updated

  cronjobs:
    rss-ingestion:
      image:
        repository: 123456.dkr.ecr.eu-central-1.amazonaws.com/social-media
        tag: "1.0.0"      # <-- updated

frontend:
  image:
    repository: social-media-frontend
    tag: "2.0.0"          # <-- NOT updated (doesn't end with "social-media")
```

`image_name: social-media` matches any `repository` ending with `social-media` (including registry-prefixed variants like `123456.dkr.ecr.../social-media`) but does **not** match `social-media-frontend`.

### With service-pipeline

Typical usage after a service-pipeline build and release:

```yaml
jobs:
  pipeline:
    uses: DND-IT/github-workflows/.github/workflows/service-pipeline.yaml@service-pipeline
    with:
      service_name: social-media
      service_path: backend
      config_path: '.github/matrix-config.yaml'
      app_id: ${{ vars.GH_APP_ID }}
    secrets:
      app_private_key: ${{ secrets.GH_APP_PRIVATE_KEY }}

  update-helm-values:
    needs: pipeline
    if: needs.pipeline.outputs.new_release_published == 'true'
    permissions:
      contents: write
      pull-requests: write
    uses: DND-IT/github-workflows/.github/workflows/gitops-image-tag.yaml@v3
    with:
      image_tag: ${{ needs.pipeline.outputs.new_release_version }}
      image_name: social-media
      values_files: |
        deploy/app/values.yaml
        deploy/app/envs/dev/values.yaml
        deploy/app/envs/prod/values.yaml
      create_pr: true
      auto_merge: true
      branch_name_prefix: helm/social-media
      app_id: ${{ vars.GH_APP_ID }}
    secrets:
      app_private_key: ${{ secrets.GH_APP_PRIVATE_KEY }}
```

### Explicit keys

Use when you need precise control over which fields to update:

```yaml
jobs:
  update-image:
    uses: DND-IT/github-workflows/.github/workflows/gitops-image-tag.yaml@v3
    with:
      image_tag: "1.2.0"
      image_tag_keys: |
        generic.image.tag
        generic.cronjobs.draft-cleanup.image.tag
      values_files: deploy/app/values.yaml
      create_pr: true
```

### Multiple files

```yaml
jobs:
  update-all-environments:
    uses: DND-IT/github-workflows/.github/workflows/gitops-image-tag.yaml@v3
    with:
      image_tag: ${{ inputs.image_tag }}
      image_tag_keys: app.image.tag
      values_files: |
        deploy/dev/values.yaml
        deploy/staging/values.yaml
        deploy/prod/values.yaml
      create_pr: true
```

### Auto-merge

```yaml
jobs:
  deploy:
    uses: DND-IT/github-workflows/.github/workflows/gitops-image-tag.yaml@v3
    with:
      image_tag: ${{ github.event.release.tag_name }}
      image_name: my-service
      values_files: deploy/prod/values.yaml
      create_pr: true
      auto_merge: true
      app_id: ${{ vars.GH_APP_ID }}
    secrets:
      app_private_key: ${{ secrets.GH_APP_PRIVATE_KEY }}
```

## How it works

1. For each file in `values_files`:
    - **Image name mode**: Uses `yq` to recursively find all objects with `repository` and `tag` fields where `repository` ends with the given `image_name`. Extracts the dot-notation path to each `tag` field.
    - **Explicit keys mode**: Uses each key from `image_tag_keys` directly.
2. For each tag field found, gets the exact line number via `yq ... | line`.
3. Uses `sed` on that specific line to replace the value, preserving indentation and formatting.
4. Creates a PR (or commits directly) with the changes.

## Key Features

### Image name search

The `image_name` input automatically discovers all image references in a values file, including deeply nested ones like cronjob images. No need to manually list every key path — add a new cronjob with the same image and it gets picked up automatically.

### Automatic PR replacement

The workflow generates consistent branch names based on the files being updated. If you update the same files again, the new PR will replace the old one. No accumulating duplicate PRs.

### Formatting preservation

Unlike a pure `yq` write which can reformat the entire file, this workflow uses `yq` only to locate the target line and `sed` to perform the replacement. This preserves comments, indentation, and quoting style.

## FAQ

**Q: When should I use `image_name` vs `image_tag_keys`?**

A: Use `image_name` (recommended) when all images sharing a name should have the same tag. Use `image_tag_keys` when you need to update specific keys that don't follow the `repository`/`tag` pattern, or when different images with similar names need different tags.

**Q: How does `image_name` matching work?**

A: It uses a regex `test("name$")` — matching any `repository` value that **ends with** the given name. This handles both plain names (`social-media`) and registry-prefixed names (`123456.dkr.ecr.eu-central-1.amazonaws.com/social-media`).

**Q: What happens if a key doesn't exist in a file?**

A: In explicit keys mode, the workflow skips that key and logs a message. In image name mode, if no matching image blocks are found in a file, it skips the entire file.

**Q: Will this create multiple PRs if I run it multiple times?**

A: No, the workflow uses consistent branch naming based on the files being updated. Running it again will update the existing PR.

**Q: Can I use both `image_name` and `image_tag_keys`?**

A: If both are provided, `image_name` takes precedence and `image_tag_keys` is ignored.
