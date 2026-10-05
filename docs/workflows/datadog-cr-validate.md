---
title: Datadog CR Validate
---

## Description

Render Helm charts containing Datadog Operator custom resources (`DatadogMonitor`, `DatadogDashboard`, `DatadogAgent`) and validate them before they reach a cluster. A resource can satisfy the CRD schema and still be rejected by the Datadog API, which leaves the operator in a reconcile error loop, so the workflow checks several layers:

1. **CRD schemas**: every rendered resource is validated with `kubeconform -strict` against the Kubernetes schemas and the [datreeio/CRDs-catalog](https://github.com/datreeio/CRDs-catalog).
2. **Dashboard lint**: `spec.widgets` must be a JSON array, every widget needs a `definition.type`, and every `$variable` used in a widget must be declared in `spec.templateVariables`. Datadog has no public validation endpoint for dashboards.
3. **Monitor validation**: every `DatadogMonitor` is converted to the API payload the operator sends and posted to Datadog's `POST /api/v1/monitor/validate` endpoint, which catches invalid queries and option combinations the schema allows.
4. **Metric and tag check** (`check_tag_values: true`): every metric used in a monitor or dashboard query must have reported data in the last 7 days, otherwise the job fails. Tag filters such as `{condition:ready}` that have not been indexed for that metric in the same window produce a warning, since tags for rare events (for example `reason:oomkilled`) can legitimately be absent.

All layers after rendering run even when an earlier one fails, so one run reports every problem.

The Datadog keys are never stored as GitHub secrets. The workflow assumes `aws_oidc_role_arn` (or the `DD_CR_VALIDATE_ROLE_ARN` organization variable) through GitHub OIDC and reads them from the `dd_keys_secret_name` secret in AWS Secrets Manager. The role must trust this workflow for the calling repository, and the calling workflow must grant `id-token: write`.

<!-- action-docs-inputs source=".github/workflows/datadog-cr-validate.yaml" -->
### Inputs

| name | description | type | required | default |
| --- | --- | --- | --- | --- |
| `charts` | <p>Helm charts to render and validate, one per line: a chart path, optionally followed by extra <code>helm template</code> arguments. Example: |   deploy/datadog-monitoring   deploy/datadog-agent --set clusterName=validate</p> | `string` | `true` | `""` |
| `check_tag_values` | <p>Fail when a metric query uses a metric that has not been reported in the last 7 days, and warn when it filters on a tag value not indexed in that window</p> | `boolean` | `false` | `false` |
| `dd_site` | <p>Datadog site to validate against. Falls back to vars.dd_site, then datadoghq.eu</p> | `string` | `false` | `""` |
| `aws_oidc_role_arn` | <p>IAM role assumed through GitHub OIDC to read the Datadog keys. Falls back to <code>vars.DD_CR_VALIDATE_ROLE_ARN</code></p> | `string` | `false` | `""` |
| `aws_region` | <p>AWS region of the Datadog keys secret</p> | `string` | `false` | `eu-central-1` |
| `dd_keys_secret_name` | <p>Secrets Manager secret holding the Datadog keys as JSON with <code>DD_API_KEY</code> and <code>DD_APP_KEY</code></p> | `string` | `false` | `dai/datadog/crValidateKeys` |
<!-- action-docs-inputs source=".github/workflows/datadog-cr-validate.yaml" -->

<!-- action-docs-outputs source=".github/workflows/datadog-cr-validate.yaml" -->

<!-- action-docs-outputs source=".github/workflows/datadog-cr-validate.yaml" -->

<!-- action-docs-usage source=".github/workflows/datadog-cr-validate.yaml" project="dnd-it/github-workflows/.github/workflows/datadog-cr-validate.yaml" version="v2" -->
### Usage

```yaml
jobs:
  job1:
    uses: dnd-it/github-workflows/.github/workflows/datadog-cr-validate.yaml@v2
    with:
      charts:
      # Helm charts to render and validate, one per line: a chart path, optionally followed by extra `helm template` arguments.
      # Example: |
      #   deploy/datadog-monitoring
      #   deploy/datadog-agent --set clusterName=validate
      #
      # Type: string
      # Required: true
      # Default: ""

      check_tag_values:
      # Fail when a metric query uses a metric that has not been reported in the last 7 days, and warn when it filters on a tag value not indexed in that window
      #
      # Type: boolean
      # Required: false
      # Default: false

      dd_site:
      # Datadog site to validate against. Falls back to vars.dd_site, then datadoghq.eu
      #
      # Type: string
      # Required: false
      # Default: ""

      aws_oidc_role_arn:
      # IAM role assumed through GitHub OIDC to read the Datadog keys. Falls back to `vars.DD_CR_VALIDATE_ROLE_ARN`
      #
      # Type: string
      # Required: false
      # Default: ""

      aws_region:
      # AWS region of the Datadog keys secret
      #
      # Type: string
      # Required: false
      # Default: eu-central-1

      dd_keys_secret_name:
      # Secrets Manager secret holding the Datadog keys as JSON with `DD_API_KEY` and `DD_APP_KEY`
      #
      # Type: string
      # Required: false
      # Default: dai/datadog/crValidateKeys
```
<!-- action-docs-usage source=".github/workflows/datadog-cr-validate.yaml" project="dnd-it/github-workflows/.github/workflows/datadog-cr-validate.yaml" version="v2" -->

## Example

### Validate on pull requests and on a schedule

```yaml
on:
  pull_request:
    paths:
      - deploy/datadog-monitoring/**
      - .github/workflows/datadog-validate.yaml
  schedule:
    - cron: "0 6 * * 1"

permissions:
  contents: read
  id-token: write

jobs:
  validate:
    uses: DND-IT/github-workflows/.github/workflows/datadog-cr-validate.yaml@datadog-cr-validate-v0
    with:
      charts: deploy/datadog-monitoring
```

The schedule catches upstream CRD schema changes even when nothing in the repository changed.

### Several charts with extra Helm arguments

```yaml
jobs:
  validate:
    uses: DND-IT/github-workflows/.github/workflows/datadog-cr-validate.yaml@datadog-cr-validate-v0
    with:
      charts: |
        configs/datadog-monitoring
        configs/datadog-agent --set clusterName=validate --set-string awsAccountId=000000000000
      check_tag_values: true
```

## FAQ

### Q: How are the extra Helm arguments parsed?

A: Each line is split on whitespace: the first word is the chart path and the rest are passed to `helm template` unchanged. Values containing spaces are not supported; put them in a values file and pass `-f path/to/values.yaml` instead.

### Q: Does it build chart dependencies?

A: No. Charts are rendered with `helm template` as they are checked out, so a chart with dependencies needs its `charts/` directory available.

### Q: Why does "Configure AWS credentials" fail?

A: Either the calling workflow does not grant `id-token: write`, neither `aws_oidc_role_arn` nor the `DD_CR_VALIDATE_ROLE_ARN` variable is set, or the role does not trust the calling repository. The schema and dashboard checks still run and report their results.

### Q: Which Datadog site is used?

A: `dd_site` if set, then the `dd_site` repository or environment variable, then `datadoghq.eu`.

### Q: Why does a monitor pass the schema check but fail validation?

A: The CRD only checks the shape of the resource. The Datadog API also parses the query and checks the options against the monitor type, which is the same validation the operator hits when it reconciles the resource. The error returned by the API is shown as an annotation on the run.

### Q: Does validation create anything in Datadog?

A: No. The monitor validation endpoint and the metric tags endpoint are read-only.
