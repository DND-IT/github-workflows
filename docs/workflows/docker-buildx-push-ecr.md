---
title: Docker Multi-Arch Build and Push to ECR
---

## Description

<!-- action-docs-inputs source=".github/workflows/docker-buildx-push-ecr.yaml" -->
### Inputs

| name | description | type | required | default |
| --- | --- | --- | --- | --- |
| `environment` | <p>Environment to run the build in</p> | `string` | `false` | `""` |
| `aws_account_id` | <p>AWS Account ID</p> | `string` | `false` | `""` |
| `aws_region` | <p>AWS Region</p> | `string` | `false` | `""` |
| `aws_role_name` | <p>AWS Role Name</p> | `string` | `false` | `""` |
| `aws_oidc_role_arn` | <p>AWS OIDC IAM role to assume</p> | `string` | `false` | `""` |
| `image_name` | <p>Name of the Docker image to build</p> | `string` | `false` | `""` |
| `image_tag` | <p>Tag of the Docker image to build</p> | `string` | `false` | `""` |
| `docker_context` | <p>Path to the build context</p> | `string` | `false` | `""` |
| `dockerfile_path` | <p>Path to the Dockerfile. If not defined, will default to {docker_context}/Dockerfile</p> | `string` | `false` | `""` |
| `docker_push` | <p>Push Image to ECR</p> | `boolean` | `false` | `true` |
| `docker_target` | <p>Build target</p> | `string` | `false` | `""` |
| `docker_platforms` | <p>Build Platforms</p> | `choice` | `false` | `linux/amd64` |
| `artifact_name` | <p>Artifact name to be downloaded before building</p> | `string` | `false` | `""` |
| `artifact_path` | <p>Artifact target path</p> | `string` | `false` | `""` |
| `artifact_pattern` | <p>A glob pattern to the artifacts that should be downloaded. Ignored if name is specified.</p> | `string` | `false` | `""` |
| `artifact_merge_multiple` | <p>When multiple artifacts are matched, this changes the behavior of the destination directories. If true, the downloaded artifacts will be in the same directory specified by path. If false, the downloaded artifacts will be extracted into individual named directories within the specified path. Optional. Default is 'false'.</p> | `boolean` | `false` | `""` |
<!-- action-docs-inputs source=".github/workflows/docker-buildx-push-ecr.yaml" -->

<!-- action-docs-outputs source=".github/workflows/docker-buildx-push-ecr.yaml" -->

<!-- action-docs-outputs source=".github/workflows/docker-buildx-push-ecr.yaml" -->

<!-- action-docs-usage source=".github/workflows/docker-buildx-push-ecr.yaml" project="tx-pts-dai/github-workflows/.github/workflows/docker-buildx-push-ecr.yaml" version="v2" -->
### Usage

```yaml
jobs:
  job1:
    uses: tx-pts-dai/github-workflows/.github/workflows/docker-buildx-push-ecr.yaml@v2
    with:
      environment:
      # Environment to run the build in
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

      image_name:
      # Name of the Docker image to build
      #
      # Type: string
      # Required: false
      # Default: ""

      image_tag:
      # Tag of the Docker image to build
      #
      # Type: string
      # Required: false
      # Default: ""

      docker_context:
      # Path to the build context
      #
      # Type: string
      # Required: false
      # Default: ""

      dockerfile_path:
      # Path to the Dockerfile. If not defined, will default to {docker_context}/Dockerfile
      #
      # Type: string
      # Required: false
      # Default: ""

      docker_push:
      # Push Image to ECR
      #
      # Type: boolean
      # Required: false
      # Default: true

      docker_target:
      # Build target
      #
      # Type: string
      # Required: false
      # Default: ""

      docker_platforms:
      # Build Platforms
      #
      # Type: choice
      # Required: false
      # Default: linux/amd64

      artifact_name:
      # Artifact name to be downloaded before building
      #
      # Type: string
      # Required: false
      # Default: ""

      artifact_path:
      # Artifact target path
      #
      # Type: string
      # Required: false
      # Default: ""

      artifact_pattern:
      # A glob pattern to the artifacts that should be downloaded. Ignored if name is specified.
      #
      # Type: string
      # Required: false
      # Default: ""

      artifact_merge_multiple:
      # When multiple artifacts are matched, this changes the behavior of the destination directories. If true, the downloaded artifacts will be in the same directory specified by path. If false, the downloaded artifacts will be extracted into individual named directories within the specified path. Optional. Default is 'false'.
      #
      # Type: boolean
      # Required: false
      # Default: ""
```
<!-- action-docs-usage source=".github/workflows/docker-buildx-push-ecr.yaml" project="tx-pts-dai/github-workflows/.github/workflows/docker-buildx-push-ecr.yaml" version="v2" -->

## Example

## FAQ
