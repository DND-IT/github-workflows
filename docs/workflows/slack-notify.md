---
title: Slack Notification
---

## Description

<!-- action-docs-inputs source=".github/workflows/slack-notify.yaml" -->
### Inputs

| name | description | type | required | default |
| --- | --- | --- | --- | --- |
| `channel` | <p>Slack channel ID or name to send notification to</p> | `string` | `true` | `""` |
| `notification_title` | <p>Title of the notification (shown in header)</p> | `string` | `true` | `""` |
| `notification_message` | <p>Main notification message text</p> | `string` | `false` | `""` |
| `status` | <p>Overall status (success, failure, partial, warning, info). Used for color and emoji if not overridden.</p> | `string` | `false` | `info` |
| `color` | <p>Custom hex color for notification (e.g., #36a64f). Overrides status-based color.</p> | `string` | `false` | `""` |
| `emoji` | <p>Custom emoji for notification. Overrides status-based emoji.</p> | `string` | `false` | `""` |
| `job_results` | <p>JSON array of job results: [{"name": "Job Name", "result": "success"}]. Max 10 fields due to Slack limits.</p> | `string` | `false` | `""` |
| `additional_fields` | <p>JSON array of custom fields: [{"name": "Field Name", "value": "Field Value"}]. Combined with job_results, max 10 total.</p> | `string` | `false` | `""` |
| `include_workflow_link` | <p>Include link to workflow run</p> | `boolean` | `false` | `true` |
| `include_triggered_by` | <p>Include information about who/what triggered the workflow</p> | `boolean` | `false` | `true` |
| `custom_blocks` | <p>JSON array of custom Slack blocks to append to the message</p> | `string` | `false` | `""` |
| `thread_ts` | <p>Thread timestamp to reply in a thread</p> | `string` | `false` | `""` |
| `environment` | <p>Environment name (optional, added as a field if provided)</p> | `string` | `false` | `""` |
<!-- action-docs-inputs source=".github/workflows/slack-notify.yaml" -->

<!-- action-docs-outputs source=".github/workflows/slack-notify.yaml" -->

<!-- action-docs-outputs source=".github/workflows/slack-notify.yaml" -->

<!-- action-docs-usage source=".github/workflows/slack-notify.yaml" project="dnd-it/github-workflows/.github/workflows/slack-notify.yaml" version="v2" -->
### Usage

```yaml
jobs:
  job1:
    uses: dnd-it/github-workflows/.github/workflows/slack-notify.yaml@v2
    with:
      channel:
      # Slack channel ID or name to send notification to
      #
      # Type: string
      # Required: true
      # Default: ""

      notification_title:
      # Title of the notification (shown in header)
      #
      # Type: string
      # Required: true
      # Default: ""

      notification_message:
      # Main notification message text
      #
      # Type: string
      # Required: false
      # Default: ""

      status:
      # Overall status (success, failure, partial, warning, info). Used for color and emoji if not overridden.
      #
      # Type: string
      # Required: false
      # Default: info

      color:
      # Custom hex color for notification (e.g., #36a64f). Overrides status-based color.
      #
      # Type: string
      # Required: false
      # Default: ""

      emoji:
      # Custom emoji for notification. Overrides status-based emoji.
      #
      # Type: string
      # Required: false
      # Default: ""

      job_results:
      # JSON array of job results: [{"name": "Job Name", "result": "success"}]. Max 10 fields due to Slack limits.
      #
      # Type: string
      # Required: false
      # Default: ""

      additional_fields:
      # JSON array of custom fields: [{"name": "Field Name", "value": "Field Value"}]. Combined with job_results, max 10 total.
      #
      # Type: string
      # Required: false
      # Default: ""

      include_workflow_link:
      # Include link to workflow run
      #
      # Type: boolean
      # Required: false
      # Default: true

      include_triggered_by:
      # Include information about who/what triggered the workflow
      #
      # Type: boolean
      # Required: false
      # Default: true

      custom_blocks:
      # JSON array of custom Slack blocks to append to the message
      #
      # Type: string
      # Required: false
      # Default: ""

      thread_ts:
      # Thread timestamp to reply in a thread
      #
      # Type: string
      # Required: false
      # Default: ""

      environment:
      # Environment name (optional, added as a field if provided)
      #
      # Type: string
      # Required: false
      # Default: ""
```
<!-- action-docs-usage source=".github/workflows/slack-notify.yaml" project="dnd-it/github-workflows/.github/workflows/slack-notify.yaml" version="v2" -->

## Examples

### Basic Success Notification

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Deploy
        run: ./deploy.sh

  notify:
    needs: [deploy]
    if: always()
    uses: dnd-it/github-workflows/.github/workflows/slack-notify.yaml@v2
    secrets:
      slack_bot_token: ${{ secrets.SLACK_BOT_TOKEN }}
    with:
      channel: "deployments"
      notification_title: "Deployment Complete"
      status: "success"
```

### Multi-Job Status Notification

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Build
        run: npm run build

  test:
    runs-on: ubuntu-latest
    steps:
      - name: Test
        run: npm test

  deploy:
    runs-on: ubuntu-latest
    needs: [build, test]
    steps:
      - name: Deploy
        run: ./deploy.sh

  notify:
    needs: [build, test, deploy]
    if: always()
    uses: dnd-it/github-workflows/.github/workflows/slack-notify.yaml@v2
    secrets:
      slack_bot_token: ${{ secrets.SLACK_BOT_TOKEN }}
    with:
      channel: "C09L9PHJ2E9"
      notification_title: "CI/CD Pipeline Status"
      notification_message: "Pipeline execution completed"
      status: "${{ needs.deploy.result }}"
      job_results: |
        [
          {"name": "Build", "result": "${{ needs.build.result }}"},
          {"name": "Test", "result": "${{ needs.test.result }}"},
          {"name": "Deploy", "result": "${{ needs.deploy.result }}"}
        ]
```

### Custom Fields and Environment

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production
    steps:
      - name: Deploy to Production
        run: ./deploy.sh

  notify:
    needs: [deploy]
    if: always()
    uses: dnd-it/github-workflows/.github/workflows/slack-notify.yaml@v2
    secrets:
      slack_bot_token: ${{ secrets.SLACK_BOT_TOKEN }}
    with:
      channel: "production-alerts"
      notification_title: "Production Deployment"
      environment: "production"
      status: "${{ needs.deploy.result }}"
      additional_fields: |
        [
          {"name": "Version", "value": "v${{ github.ref_name }}"},
          {"name": "Deployed By", "value": "${{ github.actor }}"},
          {"name": "Commit", "value": "${{ github.sha }}"}
        ]
```

### Custom Styling

```yaml
jobs:
  security_scan:
    runs-on: ubuntu-latest
    steps:
      - name: Run Security Scan
        run: ./scan.sh

  notify:
    needs: [security_scan]
    if: always()
    uses: dnd-it/github-workflows/.github/workflows/slack-notify.yaml@v2
    secrets:
      slack_bot_token: ${{ secrets.SLACK_BOT_TOKEN }}
    with:
      channel: "security"
      notification_title: "Security Scan Results"
      status: "${{ needs.security_scan.result }}"
      color: "#8B008B"  # Custom purple color
      emoji: "🔒"       # Custom lock emoji
```

### Determining Overall Status from Multiple Jobs

```yaml
jobs:
  cleanup-kubernetes:
    runs-on: ubuntu-latest
    steps:
      - name: Cleanup
        run: ./cleanup-k8s.sh

  destroy-central:
    runs-on: ubuntu-latest
    steps:
      - name: Destroy Central Stack
        run: terraform destroy -auto-approve

  destroy-network:
    runs-on: ubuntu-latest
    steps:
      - name: Destroy Network Stack
        run: terraform destroy -auto-approve

  determine-status:
    needs: [cleanup-kubernetes, destroy-central, destroy-network]
    if: always()
    runs-on: ubuntu-latest
    outputs:
      status: ${{ steps.status.outputs.status }}
    steps:
      - name: Determine Overall Status
        id: status
        run: |
          CLEANUP_STATUS="${{ needs.cleanup-kubernetes.result }}"
          CENTRAL_STATUS="${{ needs.destroy-central.result }}"
          NETWORK_STATUS="${{ needs.destroy-network.result }}"

          if [ "$CLEANUP_STATUS" == "failure" ] || [ "$CENTRAL_STATUS" == "failure" ] || [ "$NETWORK_STATUS" == "failure" ]; then
            echo "status=failure" >> $GITHUB_OUTPUT
          elif [ "$CLEANUP_STATUS" == "success" ] && [ "$CENTRAL_STATUS" == "success" ] && [ "$NETWORK_STATUS" == "success" ]; then
            echo "status=success" >> $GITHUB_OUTPUT
          else
            echo "status=partial" >> $GITHUB_OUTPUT
          fi

  notify:
    needs: [cleanup-kubernetes, destroy-central, destroy-network, determine-status]
    if: always()
    uses: dnd-it/github-workflows/.github/workflows/slack-notify.yaml@v2
    secrets:
      slack_bot_token: ${{ secrets.SLACK_BOT_TOKEN }}
    with:
      channel: "C09L9PHJ2E9"
      notification_title: "Sandbox Cleanup"
      notification_message: "Sandbox cleanup workflow completed"
      status: "${{ needs.determine-status.outputs.status }}"
      job_results: |
        [
          {"name": "Kubernetes Cleanup", "result": "${{ needs.cleanup-kubernetes.result }}"},
          {"name": "Central Stack", "result": "${{ needs.destroy-central.result }}"},
          {"name": "Network Stack", "result": "${{ needs.destroy-network.result }}"}
        ]
```

## FAQ

### How do I get a Slack Bot Token?

1. Go to https://api.slack.com/apps
2. Create a new app or select an existing one
3. Navigate to "OAuth & Permissions"
4. Add the `chat:write` bot token scope
5. Install the app to your workspace
6. Copy the "Bot User OAuth Token" (starts with `xoxb-`)
7. Add it to your repository secrets as `SLACK_BOT_TOKEN`

### How do I find my Slack Channel ID?

1. Open Slack and navigate to the channel
2. Click the channel name at the top
3. Scroll down in the modal to find the Channel ID
4. Alternatively, you can use the channel name (e.g., "deployments")

### What are the available status values?

The workflow supports the following status values:
- `success` - Green color (#36a64f) with ✅ emoji
- `failure` - Red color (#FF0000) with ❌ emoji
- `partial` / `warning` - Orange color (#FFA500) with ⚠️ emoji
- `info` - Blue color (#0066CC) with ℹ️ emoji
- Custom status - Gray color (#808080) with ⚪ emoji

You can override the color and emoji using the `color` and `emoji` inputs.

### Can I send notifications to multiple channels?

No, each workflow call sends to a single channel. To notify multiple channels, call the workflow multiple times:

```yaml
notify-team-a:
  uses: dnd-it/github-workflows/.github/workflows/slack-notify.yaml@v2
  secrets:
    slack_bot_token: ${{ secrets.SLACK_BOT_TOKEN }}
  with:
    channel: "team-a"
    notification_title: "Deployment Complete"

notify-team-b:
  uses: dnd-it/github-workflows/.github/workflows/slack-notify.yaml@v2
  secrets:
    slack_bot_token: ${{ secrets.SLACK_BOT_TOKEN }}
  with:
    channel: "team-b"
    notification_title: "Deployment Complete"
```

### How many fields can I include?

Due to Slack's Block Kit limitations, you can include up to 10 fields total. This includes:
- Job results
- Additional fields
- Environment field (if provided)
- Triggered by field (if enabled)

The workflow will include as many fields as possible up to this limit.

### Can I customize the message format completely?

For basic customization, use the `color`, `emoji`, and field inputs. For advanced customization, you can use the `custom_blocks` input to add custom Slack Block Kit blocks to your notification.

### How do I use this with GitHub environments?

Set the `environment` input to link the workflow to a GitHub environment:

```yaml
notify:
  uses: dnd-it/github-workflows/.github/workflows/slack-notify.yaml@v2
  secrets:
    slack_bot_token: ${{ secrets.SLACK_BOT_TOKEN }}
  with:
    environment: "production"
    channel: "deployments"
    notification_title: "Production Deployment"
```

This allows you to use environment-specific secrets and variables.
