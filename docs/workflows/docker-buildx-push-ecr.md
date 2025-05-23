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
| `image_push_sha_tag` | <p>Push Image SHA as Tag to ECR</p> | `boolean` | `false` | `true` |
| `docker_context` | <p>Path to the build context</p> | `string` | `false` | `""` |
| `dockerfile_path` | <p>Path to the Dockerfile. If not defined, will default to {docker_context}/Dockerfile</p> | `string` | `false` | `""` |
| `docker_push` | <p>Push Image to ECR</p> | `boolean` | `false` | `true` |
| `docker_target` | <p>Build target</p> | `string` | `false` | `""` |
| `docker_platforms` | <p>Build Platforms. Allowed values: <code>linux/amd64</code>, <code>linux/arm64</code> and <code>linux/amd64,linux/arm64</code></p> | `string` | `false` | `linux/amd64` |
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

      image_push_sha_tag:
      # Push Image SHA as Tag to ECR
      #
      # Type: boolean
      # Required: false
      # Default: true

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
      # Build Platforms. Allowed values: `linux/amd64`, `linux/arm64` and `linux/amd64,linux/arm64`
      #
      # Type: string
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

```yaml
on: [push, pull_request]
jobs:
  docker_build_push_ecr:
    uses: ./.github/workflows/docker-buildx-push-ecr.yaml
    with:
      environment: 'production'
      aws_region: 'us-west-2'
      aws_oidc_role_arn: 'arn:aws:iam::123456789012:role/my-aws-role'
      image_name: 'my-docker-image'
      image_tag: 'latest'
      docker_context: '.'
      dockerfile_path: 'Dockerfile'
      docker_push: 'true'
      # choose the archs that you want to build
      # docker_platforms: "linux/amd64"
      # docker_platforms: "linux/arm64"
      # docker_platforms: "linux/amd64,linux/arm64"
```

## FAQ

**Q: How do I choose which architectures will be build?**

A: Using the input `docker_platforms` you can choose between `linux/amd64`, `linux/arm64` or `linux/amd64,linux/arm64` - the latter will build both architectures.

**Q: How do I specify the AWS credentials?**

A: The AWS credentials are specified using the aws_account_id, aws_region, aws_role_name, and aws_oidc_role_arn inputs.

**Q: How do I specify the Docker image name and tag?**

A: The Docker image name and tag are specified using the image_name and image_tag inputs. By default, the image name is the repository name.

**Q: How do I specify the build context and Dockerfile path?**

A: The build context and Dockerfile path are specified using the docker_context and dockerfile_path inputs. By default, the build context is . and the Dockerfile path is {docker_context}/Dockerfile.

**Q: How do I control whether the image is pushed to ECR?**

A: Whether the image is pushed to ECR is controlled using the docker_push input. By default, it is set to true.

**Q: Can I only build or only push ?**

A: Yes you can call separately the workflows docker-build.yaml and docker-push-ecr.yaml. Please refer to each individual workflow for informations about inputs.

**Q: Can I pass files and folders from other jobs?**

A: Yes, you can upload them as artifacts and have the docker-build-push-ecr.yaml to download them via `artifact_path` and `artifact_name`. Example [`DND-IT/disco` PR](https://github.com/DND-IT/disco/pull/2836)
