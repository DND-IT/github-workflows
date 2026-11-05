---
title: Terraform Preview Cleanup
---

<!-- action-docs-header source=".github/workflows/tf-cleanup.yaml" -->
## Terraform Preview Cleanup
<!-- action-docs-header source=".github/workflows/tf-cleanup.yaml" -->

## Description

This workflow cleans up the Terraform preview deployments.

<!-- action-docs-inputs source=".github/workflows/tf-cleanup.yaml" -->
### Inputs

| name | description | type | required | default |
| --- | --- | --- | --- | --- |
| `environment` | <p>Environment to deploy</p> | `string` | `false` | `""` |
| `gh_deployment` | <p>Whether to create a GitHub deployment object when an environment is used.</p> | `boolean` | `false` | `true` |
| `aws_account_id` | <p>The AWS account ID.</p> | `string` | `false` | `""` |
| `aws_region` | <p>The AWS region.</p> | `string` | `false` | `""` |
| `aws_role_name` | <p>The name of the role to assume with OIDC.</p> | `string` | `false` | `""` |
| `aws_oidc_role_arn` | <p>AWS OIDC IAM role to assume</p> | `string` | `false` | `""` |
| `gh_checkout_ref` | <p>The branch, tag or SHA to checkout.</p> | `string` | `false` | `""` |
| `tf_dir` | <p>Terraform directory</p> | `string` | `false` | `""` |
| `tf_backend_configs` | <p>Terraform backend config cli arguments</p> | `string` | `false` | `""` |
| `tf_backend_config_files` | <p>List of Terraform backend config files to use, one per line. Paths should be relative to the GitHub Actions workspace.</p> | `string` | `false` | `""` |
| `tf_var_files` | <p>New line separated list of terraform variable files</p> | `string` | `false` | `""` |
| `tf_vars` | <p>New line separated list of terraform variables</p> | `string` | `false` | `""` |
| `tf_pre_run` | <p>Command to run before Terraform is executed.</p> | `string` | `false` | `""` |
| `ecr_public_login` | <p>Log in to ECR Public before Terraform runs so Helm chart pulls from public.ecr.aws are authenticated. The AWS role needs ecr-public:GetAuthorizationToken and sts:GetServiceBearerToken.</p> | `boolean` | `false` | `false` |
| `tf_workspace` | <p>Terraform workspace</p> | `string` | `false` | `""` |
| `tf_version` | <p>Terraform version to install for the workspace check. Defaults to the version the configuration asks for in required_version.</p> | `string` | `false` | `""` |
<!-- action-docs-inputs source=".github/workflows/tf-cleanup.yaml" -->

<!-- action-docs-outputs source=".github/workflows/tf-cleanup.yaml" -->

<!-- action-docs-outputs source=".github/workflows/tf-cleanup.yaml" -->

<!-- action-docs-usage source=".github/workflows/tf-cleanup.yaml" project="dnd-it/github-workflows/.github/workflows/tf-cleanup.yaml" version="v2" -->
### Usage

```yaml
jobs:
  job1:
    uses: dnd-it/github-workflows/.github/workflows/tf-cleanup.yaml@v2
    with:
      environment:
      # Environment to deploy
      #
      # Type: string
      # Required: false
      # Default: ""

      gh_deployment:
      # Whether to create a GitHub deployment object when an environment is used.
      #
      # Type: boolean
      # Required: false
      # Default: true

      aws_account_id:
      # The AWS account ID.
      #
      # Type: string
      # Required: false
      # Default: ""

      aws_region:
      # The AWS region.
      #
      # Type: string
      # Required: false
      # Default: ""

      aws_role_name:
      # The name of the role to assume with OIDC.
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

      gh_checkout_ref:
      # The branch, tag or SHA to checkout.
      #
      # Type: string
      # Required: false
      # Default: ""

      tf_dir:
      # Terraform directory
      #
      # Type: string
      # Required: false
      # Default: ""

      tf_backend_configs:
      # Terraform backend config cli arguments
      #
      # Type: string
      # Required: false
      # Default: ""

      tf_backend_config_files:
      # List of Terraform backend config files to use, one per line. Paths should be relative to the GitHub Actions workspace.
      #
      # Type: string
      # Required: false
      # Default: ""

      tf_var_files:
      # New line separated list of terraform variable files
      #
      # Type: string
      # Required: false
      # Default: ""

      tf_vars:
      # New line separated list of terraform variables
      #
      # Type: string
      # Required: false
      # Default: ""

      tf_pre_run:
      # Command to run before Terraform is executed.
      #
      # Type: string
      # Required: false
      # Default: ""

      ecr_public_login:
      # Log in to ECR Public before Terraform runs so Helm chart pulls from public.ecr.aws are authenticated. The AWS role needs ecr-public:GetAuthorizationToken and sts:GetServiceBearerToken.
      #
      # Type: boolean
      # Required: false
      # Default: false

      tf_workspace:
      # Terraform workspace
      #
      # Type: string
      # Required: false
      # Default: ""

      tf_version:
      # Terraform version to install for the workspace check. Defaults to the version the configuration asks for in required_version.
      #
      # Type: string
      # Required: false
      # Default: ""
```
<!-- action-docs-usage source=".github/workflows/tf-cleanup.yaml" project="dnd-it/github-workflows/.github/workflows/tf-cleanup.yaml" version="v2" -->

# Example

# FAQ

**Q: Terraform fails with `429 Too Many Requests` or `toomanyrequests: Data limit exceeded` when the Helm provider pulls a chart from `oci://public.ecr.aws`. How do I fix it?**

A: Set `ecr_public_login: true`. ECR Public limits how much data anonymous clients can pull from one IP address. Runners share their IP addresses, so other jobs can use up that limit. With this input, the workflow logs in to ECR Public before Terraform runs, and chart pulls use your own, higher limit. The AWS role needs `ecr-public:GetAuthorizationToken` and `sts:GetServiceBearerToken`. The token always comes from `us-east-1`, so you don't need to change `aws_region`. The login works with or without `tf_pre_run`.

```yaml
    with:
      ecr_public_login: true
```
