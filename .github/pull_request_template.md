## Description
<!--- Describe your changes in detail -->

## Motivation and Context
<!--- Why is this change required? What problem does it solve? -->
<!--- If it fixes an open issue, please link to the issue here. -->

## Breaking Changes
<!-- Does this break backwards compatibility with the current major version? -->
<!-- If so, please provide an explanation why it is necessary. -->

## How Has This Been Tested?
- [ ] I have updated at least one of the `.github/workflows/_test-*.yaml` to demonstrate and validate my change(s)
<!--- Users should start with an existing example as its written, deploy it, then check their changes against it -->
<!--- This will highlight breaking/disruptive changes. Once you have checked, deploy your changes to verify -->
<!--- Please describe how you tested your changes -->
- [ ] I have executed `pre-commit run -a` on my pull request
- [ ] I have executed `make gen_docs_run` on my pull request
<!--- Please see https://github.com/antonbabenko/pre-commit-terraform#how-to-install for how to install -->

## How Releasing Works
Releases are cut automatically on merge to `main` by [git-cliff / gh-release](https://dnd-it.github.io/github-workflows/workflows/gh-release/), driven by [Conventional Commits](https://www.conventionalcommits.org/).

**Commit type → version bump**

| Type | Bump | In changelog |
|------|------|--------------|
| `feat!:` / `BREAKING CHANGE:` | major | yes |
| `feat:` | minor | yes |
| `fix:`, `perf:`, `revert:` | patch | yes |
| `refactor:`, `docs:` | none | yes |
| `chore(deps):`, `chore(release):` | none | skipped |
| `chore:`, `ci:`, `style:`, `test:`, `build:` | none | mostly hidden |

**Choosing a merge strategy**
- **Single logical change → Squash and merge.** The PR title becomes the one conventional commit and the single changelog entry, so keep the title conventional.
- **Multiple independent fixes/features → Rebase and merge.** Each commit is preserved and itemized separately in the changelog. With squash, only the PR title survives and the other commits are lost from the notes.

**Notes**
- Multiple release-worthy commits still produce a **single release** — the highest bump wins (a `feat:` alongside `fix:`es yields one minor release).
- Changes limited to `**.md` or `docs/**` do **not** trigger a release.
