---
title: Publish TechDocs to S3
---

## Description

<!-- action-docs-inputs source=".github/workflows/techdocs-publish.yaml" -->
### Inputs

| name | description | type | required | default |
| --- | --- | --- | --- | --- |
| `entity_name` | <p>Backstage entity name (e.g. dai-handbook)</p> | `string` | `true` | `""` |
| `entity_namespace` | <p>Backstage entity namespace</p> | `string` | `false` | `default` |
| `entity_kind` | <p>Backstage entity kind</p> | `string` | `false` | `Component` |
| `requirements_file` | <p>Path to the requirements.txt file</p> | `string` | `false` | `requirements.txt` |
| `python_version` | <p>Python version</p> | `string` | `false` | `3.x` |
| `node_version` | <p>Node version for techdocs-cli</p> | `string` | `false` | `20` |
| `s3_bucket_name` | <p>S3 bucket name for TechDocs storage</p> | `string` | `true` | `""` |
| `aws_region` | <p>AWS region</p> | `string` | `false` | `eu-west-1` |
| `aws_role_arn` | <p>AWS OIDC role ARN for assuming credentials</p> | `string` | `true` | `""` |
<!-- action-docs-inputs source=".github/workflows/techdocs-publish.yaml" -->

<!-- action-docs-outputs source=".github/workflows/techdocs-publish.yaml" -->

<!-- action-docs-outputs source=".github/workflows/techdocs-publish.yaml" -->

<!-- action-docs-usage source=".github/workflows/techdocs-publish.yaml" project="dnd-it/github-workflows/.github/workflows/techdocs-publish.yaml" version="v2" -->
### Usage

```yaml
jobs:
  job1:
    uses: dnd-it/github-workflows/.github/workflows/techdocs-publish.yaml@v2
    with:
      entity_name:
      # Backstage entity name (e.g. dai-handbook)
      #
      # Type: string
      # Required: true
      # Default: ""

      entity_namespace:
      # Backstage entity namespace
      #
      # Type: string
      # Required: false
      # Default: default

      entity_kind:
      # Backstage entity kind
      #
      # Type: string
      # Required: false
      # Default: Component

      requirements_file:
      # Path to the requirements.txt file
      #
      # Type: string
      # Required: false
      # Default: requirements.txt

      python_version:
      # Python version
      #
      # Type: string
      # Required: false
      # Default: 3.x

      node_version:
      # Node version for techdocs-cli
      #
      # Type: string
      # Required: false
      # Default: 20

      s3_bucket_name:
      # S3 bucket name for TechDocs storage
      #
      # Type: string
      # Required: true
      # Default: ""

      aws_region:
      # AWS region
      #
      # Type: string
      # Required: false
      # Default: eu-west-1

      aws_role_arn:
      # AWS OIDC role ARN for assuming credentials
      #
      # Type: string
      # Required: true
      # Default: ""
```
<!-- action-docs-usage source=".github/workflows/techdocs-publish.yaml" project="dnd-it/github-workflows/.github/workflows/techdocs-publish.yaml" version="v2" -->

## Example

## FAQ
