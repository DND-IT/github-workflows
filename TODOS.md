# TODOs

## IN PROGRESS (git-ops-update branch)

### Migrate gh-release.yaml from semantic-release to git-cliff

- **Priority:** P1
- **Effort:** M (human: ~4h / CC: ~30 min)
- **Context:** Replace `cycjimmy/semantic-release-action` with `orhun/git-cliff-action@v4`. git-cliff natively supports scoped tags via `--tag-pattern` and monorepo path filtering via `--include-path`. This eliminates the Node.js dependency and simplifies scoped versioning to inputs: `service_name`, `service_path`, `cliff_config`.
- **Consolidates:** `gh-release-on-main.yaml` (manual bash versioning) into the new workflow. Port `metadata_file` support.
- **Breaking change:** Ships as `v4`. Callers on `@v3` unaffected. New inputs replace `use_semantic_release`, `tag_format`.
- **First release handling:** Auto-creates `0.1.0` when no prior tags exist.

### Rewrite gitops-image-tag.yaml to use action-yaml-update

- **Priority:** P1
- **Effort:** M (human: ~4h / CC: ~20 min)
- **Context:** The current `gitops-image-tag.yaml` manually implements YAML updating with yq/sed and PR creation with peter-evans/create-pull-request (~160 lines). The `dnd-it/action-yaml-update@v0` action already handles all of this natively with better format preservation and support for key, image, and marker modes. The rewrite simplifies the workflow to ~40 lines: app-token → checkout → action-yaml-update.
- **Interface change:** Simplified inputs to mirror action-yaml-update. Breaking change — ships under `v4`.

### Add argocd_server input to service-pipeline.yaml

- **Priority:** P1
- **Effort:** S (human: ~30min / CC: ~5 min)
- **Context:** The `service-pipeline.yaml` has built-in ArgoCD support via `argocd_app_name` input, but it doesn't accept or forward `argocd_server` to `argocd-cli.yaml`. Repos that need to pass a custom ArgoCD server URL (e.g., `${{ vars.ARGOCD_URL }}`) are forced to call `argocd-cli.yaml` directly, duplicating the ArgoCD job in each workflow file.
- **Change:** Add optional `argocd_server` input, forward it to the internal `argocd-cli.yaml` call. Non-breaking additive change.

### Document scoped tagging convention + migration guide

- **Priority:** P1
- **Effort:** S (human: ~1h / CC: ~10 min)
- **Context:** Teams using `github-workflows` need documentation on: (1) scoped tagging convention (`{service_name}-v{version}` via git-cliff), (2) migration guide from `@v3` semantic-release to `@v4` git-cliff with before/after workflow examples.
- **Tag format:** `{service_name}-v{version}` (single dash separator, e.g., `gitops-image-tag-v2.0.0`). No prefix when `service_name` is empty (whole-repo mode, e.g., `v4.0.0`).
- **Where:** `docs/VERSIONING.md` + migration section

### Update release.yaml for this repo's own v4 release

- **Priority:** P1
- **Effort:** S (human: ~15min / CC: ~5 min)
- **Context:** This repo's `release.yaml` calls `gh-release.yaml` with `use_semantic_release: true`. After the git-cliff migration, update to pass the new inputs (`service_name`, `cliff_config`). The first release after merge should create `v4.0.0`.

### Rewrite _test-gh.yaml for git-cliff

- **Priority:** P1
- **Effort:** S (human: ~1h / CC: ~10 min)
- **Context:** Existing tests validate semantic-release dry-run and custom tag format. Rewrite to test git-cliff: conventional commit bump, scoped tag creation, dry-run mode, first release (0.1.0 default).

### Create _test-gitops-image-tag.yaml

- **Priority:** P1
- **Effort:** S (human: ~2h / CC: ~15 min)
- **Context:** No test file exists for `gitops-image-tag.yaml`. After rewrite to `action-yaml-update`, add 2-3 integration tests: image_name search mode, explicit keys mode, PR creation. Tests verify workflow wiring, not action internals.

### Add cliff.toml for this repo's own releases

- **Priority:** P1
- **Effort:** S (human: ~30min / CC: ~5 min)
- **Context:** The git-cliff workflow embeds a default config for callers, but this repo should have its own `cliff.toml` to control changelog format (grouping by workflow category, conventional commit types). Used by `release.yaml`.

---

## BACKLOG

### Test coverage for scoped tag alias updates

- **Priority:** P2
- **Effort:** S (human: ~1h / CC: ~10 min)
- **Context:** The `update_version_aliases` step force-pushes alias tags (e.g., `service-name-v1`). Add test jobs to `_test-gh.yaml` that verify aliases are correctly created/updated for scoped releases. The alias logic is the most force-push-heavy part — a bug here could overwrite wrong tags.
- **Depends on:** git-cliff migration (above)

### Migrate aws-rds-version-management.yaml and tf-cleanup.yaml from sed to dedicated actions

- **Priority:** P3
- **Effort:** M (human: ~4h / CC: ~20 min)
- **Context:** These workflows use manual `sed` for YAML/config editing. For consistency with the gitops-image-tag migration to `action-yaml-update`, consider migrating these too. sed-based editing is fragile and doesn't preserve YAML formatting. Note: different use cases (Terraform backend config vs Helm values) — assess each individually.
- **Depends on:** Nothing — can be done anytime
