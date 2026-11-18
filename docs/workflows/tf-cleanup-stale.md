---
title: Terraform Stale Workspace Finder
---

## Description

Finds the Terraform workspaces of preview environments that should be torn down, and returns them as a matrix for [`tf-cleanup.yaml`](tf-cleanup.md). It destroys nothing itself.

A workspace is selected when the branch it belongs to has had no commit for `max_stale_days`, or when no open pull request (or, with `require_open_pr: false`, no remote branch) maps to it any more. Workspaces are read from the S3 state bucket, so every workspace that has state for one of the `targets` is checked, including ones the on-close cleanup missed.

Each matrix entry carries `workspace`, `reason` (`stale`, `no-open-pr`, `no-branch` or `targeted`), `age_days`, and the full `target` item, so per-target destroy inputs live in the caller's `targets`.

<!-- action-docs-inputs source=".github/workflows/tf-cleanup-stale.yaml" -->
### Inputs

| name | description | type | required | default |
| --- | --- | --- | --- | --- |
| `environment` | <p>GitHub environment to run in, e.g. when the OIDC role trusts only that environment.</p> | `string` | `false` | `""` |
| `aws_account_id` | <p>The AWS account ID.</p> | `string` | `false` | `""` |
| `aws_region` | <p>The AWS region.</p> | `string` | `false` | `""` |
| `aws_role_name` | <p>The name of the role to assume with OIDC.</p> | `string` | `false` | `""` |
| `aws_oidc_role_arn` | <p>AWS OIDC IAM role to assume</p> | `string` | `false` | `""` |
| `tf_state_bucket` | <p>S3 bucket holding the Terraform state. Defaults to tf-state-<aws_account_id>.</p> | `string` | `false` | `""` |
| `tf_workspace_key_prefix` | <p>The S3 backend's workspace<em>key</em>prefix.</p> | `string` | `false` | `env:` |
| `targets` | <p>YAML list of Terraform root modules sharing the workspaces. Each item needs <code>name</code> and <code>state_key</code> (the backend <code>key</code>); any other fields are passed through to the matrix as <code>matrix.target.&lt;field&gt;</code>.</p> | `string` | `true` | `""` |
| `workspace_from_branch` | <p>Shell command that prints the workspace name for the branch in $BRANCH. Runs in the caller's checkout, so it can call a script from the repo.</p> | `string` | `false` | `printf '%s' "$BRANCH" | sed 's|/|-|g'` |
| `workspace_pattern` | <p>Extended regex a workspace must match to be considered at all.</p> | `string` | `false` | `.*` |
| `protected_workspaces` | <p>Whitespace-separated workspaces that are never selected.</p> | `string` | `false` | `default` |
| `require_open_pr` | <p>Only an open pull request keeps a workspace alive. Set to false when previews are deployed for every pushed branch.</p> | `boolean` | `false` | `true` |
| `max_stale_days` | <p>Days without a commit after which a live branch's workspace is selected.</p> | `number` | `false` | `10` |
| `min_open_prs` | <p>Fail when the GitHub API returns fewer open pull requests than this, instead of selecting every workspace. Only used with require<em>open</em>pr.</p> | `number` | `false` | `1` |
| `workspace` | <p>Select only this workspace and skip the branch and age checks. The pattern and protected list still apply.</p> | `string` | `false` | `""` |
| `max_targets` | <p>Maximum number of matrix entries returned. The rest are picked up by the next run. GitHub caps a matrix at 256.</p> | `number` | `false` | `256` |
<!-- action-docs-inputs source=".github/workflows/tf-cleanup-stale.yaml" -->

<!-- action-docs-outputs source=".github/workflows/tf-cleanup-stale.yaml" -->
### Outputs

| name | description |
| --- | --- |
| `matrix` | <p>JSON matrix <code>{"include": [{workspace, reason, age_days, target}]}</code> with one entry per workspace and target.</p> |
| `count` | <p>Number of matrix entries.</p> |
<!-- action-docs-outputs source=".github/workflows/tf-cleanup-stale.yaml" -->

<!-- action-docs-usage source=".github/workflows/tf-cleanup-stale.yaml" project="dnd-it/github-workflows/.github/workflows/tf-cleanup-stale.yaml" version="v2" -->
### Usage

```yaml
jobs:
  job1:
    uses: dnd-it/github-workflows/.github/workflows/tf-cleanup-stale.yaml@v2
    with:
      environment:
      # GitHub environment to run in, e.g. when the OIDC role trusts only that environment.
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

      tf_state_bucket:
      # S3 bucket holding the Terraform state. Defaults to tf-state-<aws_account_id>.
      #
      # Type: string
      # Required: false
      # Default: ""

      tf_workspace_key_prefix:
      # The S3 backend's workspace_key_prefix.
      #
      # Type: string
      # Required: false
      # Default: env:

      targets:
      # YAML list of Terraform root modules sharing the workspaces. Each item needs `name` and `state_key` (the backend `key`); any other fields are passed through to the matrix as `matrix.target.<field>`.
      #
      # Type: string
      # Required: true
      # Default: ""

      workspace_from_branch:
      # Shell command that prints the workspace name for the branch in $BRANCH. Runs in the caller's checkout, so it can call a script from the repo.
      #
      # Type: string
      # Required: false
      # Default: printf '%s' "$BRANCH" | sed 's|/|-|g'

      workspace_pattern:
      # Extended regex a workspace must match to be considered at all.
      #
      # Type: string
      # Required: false
      # Default: .*

      protected_workspaces:
      # Whitespace-separated workspaces that are never selected.
      #
      # Type: string
      # Required: false
      # Default: default

      require_open_pr:
      # Only an open pull request keeps a workspace alive. Set to false when previews are deployed for every pushed branch.
      #
      # Type: boolean
      # Required: false
      # Default: true

      max_stale_days:
      # Days without a commit after which a live branch's workspace is selected.
      #
      # Type: number
      # Required: false
      # Default: 10

      min_open_prs:
      # Fail when the GitHub API returns fewer open pull requests than this, instead of selecting every workspace. Only used with require_open_pr.
      #
      # Type: number
      # Required: false
      # Default: 1

      workspace:
      # Select only this workspace and skip the branch and age checks. The pattern and protected list still apply.
      #
      # Type: string
      # Required: false
      # Default: ""

      max_targets:
      # Maximum number of matrix entries returned. The rest are picked up by the next run. GitHub caps a matrix at 256.
      #
      # Type: number
      # Required: false
      # Default: 256
```
<!-- action-docs-usage source=".github/workflows/tf-cleanup-stale.yaml" project="dnd-it/github-workflows/.github/workflows/tf-cleanup-stale.yaml" version="v2" -->

## Example

A weekly sweep over two Terraform root modules that share their workspaces. Manual runs are a dry run unless `apply` is set; the job summary of `find` lists what would be destroyed.

```yaml
on:
  schedule:
    - cron: '0 23 * * 5'
  workflow_dispatch:
    inputs:
      apply:
        type: boolean
        default: false

permissions:
  id-token: write
  contents: read
  pull-requests: write

jobs:
  find:
    uses: dnd-it/github-workflows/.github/workflows/tf-cleanup-stale.yaml@v4
    with:
      aws_account_id: '123456789012'
      aws_role_name: cicd-iac
      protected_workspaces: default main staging production
      targets: |
        - name: web
          state_key: app/web/terraform.tfstate
          tf_dir: deploy/web
          tf_var_files: deploy/web/staging.tfvars
        - name: api
          state_key: app/api/terraform.tfstate
          tf_dir: deploy/api

  destroy:
    needs: find
    if: needs.find.outputs.count != '0' && (github.event_name == 'schedule' || inputs.apply)
    strategy:
      fail-fast: false
      matrix: ${{ fromJSON(needs.find.outputs.matrix) }}
    uses: dnd-it/github-workflows/.github/workflows/tf-cleanup.yaml@v4
    with:
      aws_account_id: '123456789012'
      aws_role_name: cicd-iac
      gh_deployment: false
      tf_dir: ${{ matrix.target.tf_dir }}
      tf_workspace: ${{ matrix.workspace }}
      tf_backend_configs: |
        bucket=tf-state-123456789012
        key=${{ matrix.target.state_key }}
      tf_var_files: ${{ matrix.target.tf_var_files }}
```

If previews are deployed for every pushed branch rather than per pull request, set `require_open_pr: false`. If the workspace name is not just the branch name with `/` replaced, pass `workspace_from_branch`, for example `printf 'preview-%s' "$(bash .github/scripts/branch-slug.sh "$BRANCH")"`.

## FAQ
