# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a reusable GitHub Actions workflows repository maintained by DND-IT/DAI. It provides centralized, standardized workflow templates for common CI/CD tasks that can be called from other repositories using GitHub's `workflow_call` event.

## Common Commands

```bash
# Install documentation generation tools
make gen_docs_install

# Generate workflow documentation
make gen_docs_run

# Run workflow tests (via GitHub Actions)
# Tests are automatically triggered on PRs when workflows or test files change
```

## Architecture and Key Patterns

### Workflow Organization
- **Production workflows**: `.github/workflows/<tool>-<description>.yaml`
- **Test workflows**: `.github/workflows/_test-<workflow-name>.yaml`
- **Documentation**: `docs/workflows/<workflow-name>.md` (auto-generated)

### Input Handling Pattern
All workflows use a consistent fallback pattern for inputs:
```yaml
env:
  VARIABLE: ${{ inputs.variable || vars.variable || 'default-value' }}
```
Priority: workflow inputs → GitHub environment variables → defaults

### AWS Authentication
Standardized OIDC authentication:
```yaml
ROLE_TO_ASSUME: ${{ inputs.aws_oidc_role_arn || vars.aws_oidc_role_arn || format('arn:aws:iam::{0}:role/{1}', inputs.aws_account_id, inputs.aws_role_name) }}
```

### Testing Conventions
- Each workflow has corresponding test jobs in `_test-*.yaml` files
- Tests exercise multiple scenarios: with/without environments, error cases, different configurations
- Sandbox AWS account (911453050078) used for testing
- Tests validate both success and failure paths

## Workflow Categories

1. **Terraform**: tf-plan, tf-apply, tf-feature, tf-cleanup, tf-destroy
2. **Docker**: docker-build, docker-build-push-ecr, docker-buildx-push-ecr, docker-push-ecr
3. **Lambda**: lambda-nodejs, lambda-python, lambda-build-node
4. **GitOps**: gitops-image-tag, gitops-helm-diff, gitops-kustomize-diff
5. **AWS Utilities**: aws-rds-snapshot, aws-secrets-copy
6. **Release Management**: gh-release, gh-release-on-main

## Release Process

- Triggered on PR merge to main branch
- Uses conventional commits:
  - `feat!:` → major version
  - `feat:` → minor version
  - `fix:` → patch version
- Automatic version alias updates (v1, v1.2 tags)

## Key Files to Understand

- `README.md`: Project overview and usage instructions
- `Makefile`: Build and documentation commands
- `renovate.json`: Dependency update configuration
- `mkdocs.yaml`: Documentation site configuration
- `docs/getting-started/inputs.md`: Input handling documentation
- Test fixtures in `tests/` directory for understanding workflow usage

## Important Notes

- This repository follows the "single source of truth" principle for standard workflows
- Workflows are designed to be parameterized and flexible through inputs/environment variables
- All workflows support both explicit inputs and GitHub environment-based configuration
