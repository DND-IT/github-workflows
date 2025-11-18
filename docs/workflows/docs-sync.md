---
title: Deploy to S3 & CloudFront
---

## Description

<!-- action-docs-inputs source=".github/workflows/docs-sync.yaml" -->
### Inputs

| name | description | type | required | default |
| --- | --- | --- | --- | --- |
| `environment` | <p>Environment to deploy</p> | `string` | `false` | `""` |
| `aws_account_id` | <p>AWS Account ID</p> | `string` | `false` | `""` |
| `aws_region` | <p>AWS Region</p> | `string` | `false` | `""` |
| `aws_role_name` | <p>AWS Role Name</p> | `string` | `false` | `""` |
| `aws_oidc_role_arn` | <p>AWS OIDC IAM role to assume</p> | `string` | `false` | `""` |
| `artifact_name` | <p>Name of the build artifact to deploy</p> | `string` | `true` | `""` |
| `s3_bucket` | <p>S3 bucket name</p> | `string` | `true` | `""` |
| `s3_path` | <p>Path in S3 bucket (e.g., docs/)</p> | `string` | `false` | `""` |
| `cloudfront_distribution_id` | <p>CloudFront distribution ID</p> | `string` | `true` | `""` |
| `cloudfront_paths` | <p>CloudFront invalidation paths (e.g., /docs/*)</p> | `string` | `true` | `""` |
| `delete_removed` | <p>Delete files from S3 that are not in source (--delete flag)</p> | `boolean` | `false` | `true` |
<!-- action-docs-inputs source=".github/workflows/docs-sync.yaml" -->

<!-- action-docs-outputs source=".github/workflows/docs-sync.yaml" -->

<!-- action-docs-outputs source=".github/workflows/docs-sync.yaml" -->

<!-- action-docs-usage source=".github/workflows/docs-sync.yaml" project="dnd-it/github-workflows/.github/workflows/docs-sync.yaml" version="v2" -->
### Usage

```yaml
jobs:
  job1:
    uses: dnd-it/github-workflows/.github/workflows/docs-sync.yaml@v2
    with:
      environment:
      # Environment to deploy
      #
      # Type: string
      # Required: false
      # Default: ""

      aws_account_id:
      # AWS Account ID
      #
      # Type: string
      # Required: false
      # Default: ""

      aws_region:
      # AWS Region
      #
      # Type: string
      # Required: false
      # Default: ""

      aws_role_name:
      # AWS Role Name
      #
      # Type: string
      # Required: false
      # Default: ""

      aws_oidc_role_arn:
      # AWS OIDC IAM role to assume
      #
      # Type: string
      # Required: false
      # Default: ""

      artifact_name:
      # Name of the build artifact to deploy
      #
      # Type: string
      # Required: true
      # Default: ""

      s3_bucket:
      # S3 bucket name
      #
      # Type: string
      # Required: true
      # Default: ""

      s3_path:
      # Path in S3 bucket (e.g., docs/)
      #
      # Type: string
      # Required: false
      # Default: ""

      cloudfront_distribution_id:
      # CloudFront distribution ID
      #
      # Type: string
      # Required: true
      # Default: ""

      cloudfront_paths:
      # CloudFront invalidation paths (e.g., /docs/*)
      #
      # Type: string
      # Required: true
      # Default: ""

      delete_removed:
      # Delete files from S3 that are not in source (--delete flag)
      #
      # Type: boolean
      # Required: false
      # Default: true
```
<!-- action-docs-usage source=".github/workflows/docs-sync.yaml" project="dnd-it/github-workflows/.github/workflows/docs-sync.yaml" version="v2" -->

## Example

## FAQ
