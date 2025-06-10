---
title: Update Helm Image Tag in Values.yaml
---

## Description

This GitHub Actions workflow updates the image tag in specified yaml files. It can create a pull request with the changes or commit them directly to the target branch. The workflow is designed to be reusable and can handle multiple files and keys.

<!-- action-docs-inputs source=".github/workflows/gitops-image-tag.yaml" -->
### Inputs

| name | description | type | required | default |
| --- | --- | --- | --- | --- |
| `image_tag` | <p>The tag of the Docker image</p> | `string` | `true` | `""` |
| `image_tag_keys` | <p>Newline-separated list of keys to update (e.g., webapp.image.tag)</p> | `string` | `false` | `webapp.image_tag` |
| `values_files` | <p>Newline-separated list of file paths to update</p> | `string` | `false` | `deploy/app/values.yaml` |
| `create_pr` | <p>Create a pull request. If false, the changes will be committed directly to the target branch. Github Actions must have write permissions to the repository and able to bypass branch protection rules.</p> | `boolean` | `false` | `true` |
| `pr_message` | <p>Custom message for the pull request. Defaults to a standard message.</p> | `string` | `false` | `This PR updates the Helm values files to use the latest image tag.` |
| `target_branch` | <p>The target branch for the pull request. Defaults the default branch of the repository.</p> | `string` | `false` | `${{ github.event.repository.default_branch }}` |
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

      image_tag_keys:
      # Newline-separated list of keys to update (e.g., webapp.image.tag)
      #
      # Type: string
      # Required: false
      # Default: webapp.image_tag

      values_files:
      # Newline-separated list of file paths to update
      #
      # Type: string
      # Required: false
      # Default: deploy/app/values.yaml

      create_pr:
      # Create a pull request. If false, the changes will be committed directly to the target branch.
      # Github Actions must have write permissions to the repository and able to bypass branch protection rules.
      #
      # Type: boolean
      # Required: false
      # Default: true

      pr_message:
      # Custom message for the pull request. Defaults to a standard message.
      #
      # Type: string
      # Required: false
      # Default: This PR updates the Helm values files to use the latest image tag.

      target_branch:
      # The target branch for the pull request. Defaults the default branch of the repository.
      #
      # Type: string
      # Required: false
      # Default: ${{ github.event.repository.default_branch }}
```
<!-- action-docs-usage source=".github/workflows/gitops-image-tag.yaml" project="dnd-it/github-workflows/.github/workflows/gitops-image-tag.yaml" version="v2" -->

## Examples

### Single File Update

```yaml
name: Update Image Tag
on:
  workflow_run:
    workflows: ["Build and Push Docker Image"]
    types:
      - completed

permissions:
  contents: write
  pull-requests: write

jobs:
  update-image:
    uses: dnd-it/github-workflows/.github/workflows/gitops-image-tag.yaml@v3
    with:
      image_tag: ${{ github.sha }}
      values_files: deploy/app/values.yaml
      image_tag_keys: image_tag
      create_pr: true
```

### Multiple Files Update

```yaml
name: Update Image Tag in Multiple Environments
on:
  workflow_dispatch:
    inputs:
      image_tag:
        description: 'Docker image tag to deploy'
        required: true

permissions:
  contents: write
  pull-requests: write

jobs:
  update-all-environments:
    uses: dnd-it/github-workflows/.github/workflows/gitops-image-tag.yaml@v3
    with:
      image_tag: ${{ inputs.image_tag }}
      values_files: |
        deploy/dev/values.yaml
        deploy/staging/values.yaml
        deploy/prod/values.yaml
      image_tag_keys: "app.image.tag"
      create_pr: true
```

This creates a single PR that updates the image tag across all environment files, making it easy to promote a specific version across environments.

### Multiple Keys Update

```yaml
name: Update Multiple Image Tags
on:
  workflow_dispatch:
    inputs:
      image_tag:
        description: 'Docker image tag'
        required: true

permissions:
  contents: write
  pull-requests: write

jobs:
  update-multiple-keys:
    uses: dnd-it/github-workflows/.github/workflows/gitops-image-tag.yaml@v3
    with:
      image_tag: ${{ inputs.image_tag }}
      image_tag_keys: |
        webapp.image.tag
        worker.image.tag
        api.image.tag
      values_files: deploy/app/values.yaml
      create_pr: true
```

This updates multiple services that share the same Docker image.

## Key Features

### Automatic PR Replacement

The workflow now generates consistent branch names based on the files being updated. This means:
- If you update the same files again, the new PR will replace the old one
- No more accumulating duplicate PRs for the same files
- Branch names are based on a hash of the files being updated

### Multiple Files Support

You can update multiple values files in a single workflow run:
- Use the `values_files` input with newline-separated file paths
- All files are updated in a single commit/PR

### Multiple Keys Support

You can update multiple keys with the same image tag:
- Use the `image_tag_keys` input with newline-separated key paths
- Useful when multiple services share the same image

### Enhanced PR Management

- Detailed PR descriptions showing all updated files
- Option to commit directly without creating a PR

## FAQ

**Q: How can I update multiple values files?**

A: Use the `values_files` input with newline-separated file paths:
```yaml
values_files: |
  file1.yaml
  file2.yaml
  file3.yaml
```

**Q: Will this create multiple PRs if I run it multiple times?**

A: No, the workflow uses consistent branch naming based on the files being updated. Running it again will update the existing PR.

**Q: Can I update multiple keys with the same image tag?**

A: Yes, use the `image_tag_keys` input with newline-separated key paths:
```yaml
image_tag_keys: |
  frontend.image.tag
  backend.image.tag
  worker.image.tag
```

**Q: What happens if a key doesn't exist in a file?**

A: The yq command will create the key path if it doesn't exist. For example, if `webapp.image.tag` doesn't exist, it will create the nested structure.

**Q: Is the values_files input required?**

A: Yes, the `values_files` input is required. You must specify at least one file path to update.
