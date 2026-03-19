---
title: Kubernetes Health Check
---

<!-- action-docs-header source=".github/workflows/k8s-health-check.yaml" -->
## Kubernetes Health Check
<!-- action-docs-header source=".github/workflows/k8s-health-check.yaml" -->

## Description

Validates that key cluster components are healthy after a Terraform apply.
Intended to run after `tf-apply` for the platform stack and gate the prod apply on dev health.

Checks performed:
- **Karpenter** — controller Deployment rollout (`kube-system`)
- **Datadog** — operator Deployment, cluster-agent Deployment, node-agent DaemonSet rollout (`monitoring`); operator log scan for reconciliation errors
- **Lacework** — node-agent DaemonSet and cluster Deployment rollout (`lacework`); skipped gracefully if not deployed

## Usage

```yaml
jobs:
  apply-dev:
    uses: DND-IT/github-workflows/.github/workflows/tf-apply.yaml@v3
    with:
      environment: platform-dev

  health-check-dev:
    needs: apply-dev
    uses: DND-IT/github-workflows/.github/workflows/k8s-health-check.yaml@v3
    with:
      environment: platform-dev

  apply-prod:
    needs: health-check-dev
    uses: DND-IT/github-workflows/.github/workflows/tf-apply.yaml@v3
    with:
      environment: platform-prod
```

<!-- action-docs-inputs source=".github/workflows/k8s-health-check.yaml" -->
### Inputs

| name | description | type | required | default |
| --- | --- | --- | --- | --- |
| `environment` | <p>GitHub environment to use for resolving variables (AWS_OIDC_ROLE_ARN, AWS_REGION).</p> | `string` | `false` | `""` |
| `aws_account_id` | <p>The AWS account ID.</p> | `string` | `false` | `""` |
| `aws_region` | <p>The AWS region.</p> | `string` | `false` | `""` |
| `aws_role_name` | <p>The name of the role to assume with OIDC.</p> | `string` | `false` | `""` |
| `aws_oidc_role_arn` | <p>AWS OIDC IAM role to assume.</p> | `string` | `false` | `""` |
<!-- action-docs-inputs source=".github/workflows/k8s-health-check.yaml" -->
