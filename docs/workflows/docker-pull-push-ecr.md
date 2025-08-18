---
title: Docker Pull Push ECR
---

## Description

<!-- action-docs-inputs source=".github/workflows/docker-pull-push-ecr.yaml" -->
### Inputs

| name | description | type | required | default |
| --- | --- | --- | --- | --- |
| `environment` | <p>Environment to deploy</p> | `string` | `false` | `""` |
| `source_aws_account_id` | <p>Source AWS Account ID</p> | `string` | `false` | `""` |
| `source_aws_region` | <p>Source AWS Region</p> | `string` | `false` | `""` |
| `source_aws_role_name` | <p>Source AWS Role Name</p> | `string` | `false` | `""` |
| `source_aws_oidc_role_arn` | <p>Source AWS OIDC IAM role to assume</p> | `string` | `false` | `""` |
| `source_image_name` | <p>Name of the Docker image to pull from source ECR</p> | `string` | `false` | `""` |
| `source_image_tag` | <p>Tag of the Docker image to pull</p> | `string` | `false` | `latest` |
| `dest_aws_account_id` | <p>Destination AWS Account ID</p> | `string` | `false` | `""` |
| `dest_aws_region` | <p>Destination AWS Region</p> | `string` | `false` | `""` |
| `dest_aws_role_name` | <p>Destination AWS Role Name</p> | `string` | `false` | `""` |
| `dest_aws_oidc_role_arn` | <p>Destination AWS OIDC IAM role to assume</p> | `string` | `false` | `""` |
| `dest_image_name` | <p>Name of the Docker image to push to destination ECR</p> | `string` | `false` | `""` |
| `dest_image_tag` | <p>Tag of the Docker image to push</p> | `string` | `false` | `""` |
| `artifact_name` | <p>Artifact name for the Docker image</p> | `string` | `false` | `""` |
<!-- action-docs-inputs source=".github/workflows/docker-pull-push-ecr.yaml" -->

<!-- action-docs-outputs source=".github/workflows/docker-pull-push-ecr.yaml" -->

<!-- action-docs-outputs source=".github/workflows/docker-pull-push-ecr.yaml" -->

<!-- action-docs-usage source=".github/workflows/docker-pull-push-ecr.yaml" project="dnd-it/github-workflows/.github/workflows/docker-pull-push-ecr.yaml" version="v2" -->
### Usage

```yaml
jobs:
  job1:
    uses: dnd-it/github-workflows/.github/workflows/docker-pull-push-ecr.yaml@v2
    with:
      environment:
      # Environment to deploy
      #
      # Type: string
      # Required: false
      # Default: ""

      source_aws_account_id:
      # Source AWS Account ID
      #
      # Type: string
      # Required: false
      # Default: ""

      source_aws_region:
      # Source AWS Region
      #
      # Type: string
      # Required: false
      # Default: ""

      source_aws_role_name:
      # Source AWS Role Name
      #
      # Type: string
      # Required: false
      # Default: ""

      source_aws_oidc_role_arn:
      # Source AWS OIDC IAM role to assume
      #
      # Type: string
      # Required: false
      # Default: ""

      source_image_name:
      # Name of the Docker image to pull from source ECR
      #
      # Type: string
      # Required: false
      # Default: ""

      source_image_tag:
      # Tag of the Docker image to pull
      #
      # Type: string
      # Required: false
      # Default: latest

      dest_aws_account_id:
      # Destination AWS Account ID
      #
      # Type: string
      # Required: false
      # Default: ""

      dest_aws_region:
      # Destination AWS Region
      #
      # Type: string
      # Required: false
      # Default: ""

      dest_aws_role_name:
      # Destination AWS Role Name
      #
      # Type: string
      # Required: false
      # Default: ""

      dest_aws_oidc_role_arn:
      # Destination AWS OIDC IAM role to assume
      #
      # Type: string
      # Required: false
      # Default: ""

      dest_image_name:
      # Name of the Docker image to push to destination ECR
      #
      # Type: string
      # Required: false
      # Default: ""

      dest_image_tag:
      # Tag of the Docker image to push
      #
      # Type: string
      # Required: false
      # Default: ""

      artifact_name:
      # Artifact name for the Docker image
      #
      # Type: string
      # Required: false
      # Default: ""
```
<!-- action-docs-usage source=".github/workflows/docker-pull-push-ecr.yaml" project="dnd-it/github-workflows/.github/workflows/docker-pull-push-ecr.yaml" version="v2" -->

## Example

## FAQ
