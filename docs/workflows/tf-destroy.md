---
title: Terraform Destroy
---

<!-- action-docs-header source=".github/workflows/tf-destroy.yaml" -->
## Terraform Destroy
<!-- action-docs-header source=".github/workflows/tf-destroy.yaml" -->

## Description

This workflow destroys Terraform resources.

<!-- action-docs-inputs source=".github/workflows/tf-destroy.yaml" -->
### Inputs

| name | description | type | required | default |
| --- | --- | --- | --- | --- |
| `environment` | <p>Environment to deploy.</p> | `string` | `false` | `""` |
| `gh_deployment` | <p>Whether to create a GitHub deployment object when an environment is used.</p> | `boolean` | `false` | `true` |
| `aws_account_id` | <p>The AWS account ID.</p> | `string` | `false` | `""` |
| `aws_region` | <p>The AWS region.</p> | `string` | `false` | `""` |
| `aws_role_name` | <p>The name of the role to assume with OIDC.</p> | `string` | `false` | `""` |
| `aws_oidc_role_arn` | <p>AWS OIDC IAM role to assume</p> | `string` | `false` | `""` |
| `gh_checkout_ref` | <p>The branch, tag or SHA to checkout.</p> | `string` | `false` | `""` |
| `tf_dir` | <p>Path to the Terraform root module to apply.</p> | `string` | `false` | `""` |
| `tf_backend_configs` | <p>List of Terraform backend config values, one per line.</p> | `string` | `false` | `""` |
| `tf_backend_config_files` | <p>List of Terraform backend config files to use, one per line. Paths should be relative to the GitHub Actions workspace.</p> | `string` | `false` | `""` |
| `tf_var_files` | <p>List of tfvars files to use, one per line. Paths should be relative to the GitHub Actions workspace.</p> | `string` | `false` | `""` |
| `tf_vars` | <p>Variables to set for the Terraform plan. This should be valid Terraform syntax.</p> | `string` | `false` | `""` |
| `tf_pre_run` | <p>Command to run before Terraform is executed.</p> | `string` | `false` | `""` |
| `ecr_public_login` | <p>Log in to ECR Public before Terraform runs so Helm chart pulls from public.ecr.aws are authenticated. The AWS role needs ecr-public:GetAuthorizationToken and sts:GetServiceBearerToken.</p> | `boolean` | `false` | `false` |
<!-- action-docs-inputs source=".github/workflows/tf-destroy.yaml" -->

<!-- action-docs-outputs source=".github/workflows/tf-destroy.yaml" -->

<!-- action-docs-outputs source=".github/workflows/tf-destroy.yaml" -->

<!-- action-docs-usage source=".github/workflows/tf-destroy.yaml" project="dnd-it/github-workflows/.github/workflows/tf-destroy.yaml" version="v2" -->
### Usage

```yaml
jobs:
  job1:
    uses: dnd-it/github-workflows/.github/workflows/tf-destroy.yaml@v2
    with:
      environment:
      # Environment to deploy.
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
      # Path to the Terraform root module to apply.
      #
      # Type: string
      # Required: false
      # Default: ""

      tf_backend_configs:
      # List of Terraform backend config values, one per line.
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
      # List of tfvars files to use, one per line. Paths should be relative to the GitHub Actions workspace.
      #
      # Type: string
      # Required: false
      # Default: ""

      tf_vars:
      # Variables to set for the Terraform plan. This should be valid Terraform syntax.
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
```
<!-- action-docs-usage source=".github/workflows/tf-destroy.yaml" project="dnd-it/github-workflows/.github/workflows/tf-destroy.yaml" version="v2" -->

# Example

# FAQ

**Q: Terraform fails with `429 Too Many Requests` or `toomanyrequests: Data limit exceeded` when the Helm provider pulls a chart from `oci://public.ecr.aws`. How do I fix it?**

A: Set `ecr_public_login: true`. ECR Public limits how much data anonymous clients can pull from one IP address. Runners share their IP addresses, so other jobs can use up that limit. With this input, the workflow logs in to ECR Public before Terraform runs, and chart pulls use your own, higher limit. The AWS role needs `ecr-public:GetAuthorizationToken` and `sts:GetServiceBearerToken`. The token always comes from `us-east-1`, so you don't need to change `aws_region`. The login works with or without `tf_pre_run`.

```yaml
    with:
      ecr_public_login: true
```
