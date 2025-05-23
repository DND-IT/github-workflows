---
title: Terraform Plan
---

<!-- action-docs-header source=".github/workflows/tf-plan.yaml" -->
## Terraform Plan
<!-- action-docs-header source=".github/workflows/tf-plan.yaml" -->

## Description

This workflow runs `terraform plan` and uploads the plan to Github Action summary and creates a PR comment.

<!-- action-docs-inputs source=".github/workflows/tf-plan.yaml" -->
### Inputs

| name | description | type | required | default |
| --- | --- | --- | --- | --- |
| `environment` | <p>Environment to deploy.</p> | `string` | `false` | `""` |
| `aws_account_id` | <p>The AWS account ID.</p> | `string` | `false` | `""` |
| `aws_region` | <p>The AWS region.</p> | `string` | `false` | `""` |
| `aws_role_name` | <p>The name of the role to assume with OIDC.</p> | `string` | `false` | `""` |
| `aws_oidc_role_arn` | <p>AWS OIDC IAM role to assume</p> | `string` | `false` | `""` |
| `gh_artifact_path` | <p>Path to download artifacts to. If unset, default action workspace is used. If both 'gh<em>artifact</em>path' and 'gh<em>artifact</em>name' are unset, artifacts are not downloaded.</p> | `string` | `false` | `""` |
| `gh_artifact_name` | <p>Name of the artifact to download. If only 'gh<em>artifact</em>path' is set, then all artifacts are downloaded. If both 'gh<em>artifact</em>path' and 'gh<em>artifact</em>name' are unset, artifacts are not downloaded.</p> | `string` | `false` | `""` |
| `gh_checkout_ref` | <p>The branch, tag or SHA to checkout.</p> | `string` | `false` | `""` |
| `gh_artifact_pattern` | <p>A glob pattern to the artifacts that should be downloaded. Ignored if name is specified.</p> | `string` | `false` | `""` |
| `gh_artifact_merge_multiple` | <p>When multiple artifacts are matched, this changes the behavior of the destination directories. If true, the downloaded artifacts will be in the same directory specified by path. If false, the downloaded artifacts will be extracted into individual named directories within the specified path. Optional. Default is 'false'.</p> | `boolean` | `false` | `""` |
| `gh_comment` | <p>Whether to post a comment on the PR with the Terraform plan</p> | `string` | `false` | `changes-only` |
| `tf_dir` | <p>Path to the Terraform root module to apply.</p> | `string` | `false` | `""` |
| `tf_backend_configs` | <p>List of Terraform backend config values, one per line.</p> | `string` | `false` | `""` |
| `tf_backend_config_files` | <p>List of Terraform backend config files to use, one per line. Paths should be relative to the GitHub Actions workspace.</p> | `string` | `false` | `""` |
| `tf_var_files` | <p>List of tfvars files to use, one per line. Paths should be relative to the GitHub Actions workspace.</p> | `string` | `false` | `""` |
| `tf_vars` | <p>Variables to set for the Terraform plan. This should be valid Terraform syntax.</p> | `string` | `false` | `""` |
| `tf_pre_run` | <p>Command to run before Terraform is executed.</p> | `string` | `false` | `""` |
<!-- action-docs-inputs source=".github/workflows/tf-plan.yaml" -->

<!-- action-docs-outputs source=".github/workflows/tf-plan.yaml" -->

<!-- action-docs-outputs source=".github/workflows/tf-plan.yaml" -->

<!-- action-docs-usage source=".github/workflows/tf-plan.yaml" project="dnd-it/github-workflows/.github/workflows/tf-plan.yaml" version="v2" -->
### Usage

```yaml
jobs:
  job1:
    uses: dnd-it/github-workflows/.github/workflows/tf-plan.yaml@v2
    with:
      environment:
      # Environment to deploy.
      #
      # Type: string
      # Required: false
      # Default: ""

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

      gh_artifact_path:
      # Path to download artifacts to. If unset, default action workspace is used. If both 'gh_artifact_path' and 'gh_artifact_name' are unset, artifacts are not downloaded.
      #
      # Type: string
      # Required: false
      # Default: ""

      gh_artifact_name:
      # Name of the artifact to download. If only 'gh_artifact_path' is set, then all artifacts are downloaded. If both 'gh_artifact_path' and 'gh_artifact_name' are unset, artifacts are not downloaded.
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

      gh_artifact_pattern:
      # A glob pattern to the artifacts that should be downloaded. Ignored if name is specified.
      #
      # Type: string
      # Required: false
      # Default: ""

      gh_artifact_merge_multiple:
      # When multiple artifacts are matched, this changes the behavior of the destination directories. If true, the downloaded artifacts will be in the same directory specified by path. If false, the downloaded artifacts will be extracted into individual named directories within the specified path. Optional. Default is 'false'.
      #
      # Type: boolean
      # Required: false
      # Default: ""

      gh_comment:
      # Whether to post a comment on the PR with the Terraform plan
      #
      # Type: string
      # Required: false
      # Default: changes-only

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
```
<!-- action-docs-usage source=".github/workflows/tf-plan.yaml" project="dnd-it/github-workflows/.github/workflows/tf-plan.yaml" version="v2" -->

# Example

# FAQ
