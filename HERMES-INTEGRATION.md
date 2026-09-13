# Hermes Integration Contract — Canonical COOP Standards

This bundle is owner-approved source material for the canonical standards repository.

## Repository

Create the organization-owned canonical standards repository if it does not already exist. Preferred name: `coop-standards`.

Do not invent or hard-code an inaccessible organization URL during implementation. After provisioning, pin the real remote in COOP configuration/registry and prove it with native sync evidence.

Commit these canonical files:

- `standards/sql.md`
- `standards/dax.md`
- `standards/semantic-model.md`
- `standards.yml`
- `README.md`

The uploaded Semantic Model source screenshot has been converted into machine-readable text. Do not retain the base64 image payload in the canonical standard.

## Required COOP behavior

Standards compliance is default execution behavior. The user does not need to ask COOP to check standards.

### SQL task

1. Resolve client/project override, otherwise canonical SQL standard, otherwise last-known-good/bundled fallback.
2. Load applicable mandatory SQL sections before generating or modifying SQL.
3. Generate work in conformance with that standard.
4. Run `coop-sql-review` against the exact same effective standards file/revision when deterministic review applies.
5. Preserve repository/file/commit/hash provenance.

### DAX task

1. Resolve effective DAX standard.
2. Load applicable mandatory DAX sections before generating or modifying DAX.
3. Generate work in conformance with that standard.
4. Run `coop-dax-review` against the exact same effective DAX standard/revision when deterministic review applies.
5. Preserve provenance.

### Semantic-model task

1. Resolve effective Semantic Model standard.
2. Resolve effective DAX standard.
3. Load mandatory model sections plus applicable DAX sections before generating/reviewing model changes.
4. Retrieve Incremental BI selectively as an approved pattern source when relevant; it is not formal policy.
5. Run DAX deterministic review against the same DAX revision for measure/expression changes.
6. Preserve provenance for every consulted formal standard.

## Automatic policy refresh

The approved default branch is authoritative. Pull-request branches are non-authoritative until merged.

Implement a bounded standards refresh using the existing safe knowledge/git infrastructure where practical rather than creating a second git runner.

Required behavior:

- refresh canonical standards at COOP startup when online;
- before a standards-governed task, refresh if last successful check is older than 15 minutes;
- `coop sync` forces refresh immediately;
- remote checks and git operations are bounded/non-interactive;
- a failed refresh leaves the last-known-good canonical checkout intact;
- never replace a good checkout with a partial clone/fetch;
- when commit changes, atomically activate the new revision and rebuild/invalidate the standards search index;
- pin one exact standards commit for an in-flight task;
- generation and deterministic review for that task must use the same pinned revision;
- a later task may use a newer synchronized revision;
- Doctor/Support reports repository, branch, exact commit, last successful sync/check, effective source per domain, and fallback state.

Do not fetch on every prompt. Use the freshness contract above.

## Client isolation

Each client Windows profile/VM has an isolated COOP installation and local standards cache. The same approved Cooptimize standards may synchronize into each isolated installation; client/project overrides and client-local context remain local to that installation/project.

Standards sync must use the designated Cooptimize/Git identity and must not reuse or leak client credentials into the central standards repository.

## Backward compatibility

- Existing v0.23.1-era `.coop/project.yml` standards paths remain valid as explicit project overrides.
- Keep bundled SQL/DAX standards in their reviewer packages as offline/bootstrap fallbacks until migration is fully accepted.
- Do not bulk-rewrite existing project contracts.
- Do not delete current reviewer fallbacks until the final hardening phase determines they can safely become generated release snapshots or remain deliberate fallbacks.

## Acceptance

Prove all of the following on exact candidate SHAs:

1. Fresh install synchronizes all three canonical standards.
2. SQL generation and SQL reviewer use the same canonical SQL revision.
3. DAX generation and DAX reviewer use the same canonical DAX revision.
4. Semantic-model work automatically loads Semantic Model + DAX policy.
5. Merge a harmless standards fixture change to the authoritative test branch/repo; a subsequent COOP task detects the new commit without reinstall/update and uses the new rule.
6. An open/unmerged standards PR is not applied automatically.
7. A standards change during an in-flight task does not change that task's pinned revision.
8. Offline/network failure uses last-known-good and reports degraded freshness truthfully.
9. First-ever sync failure may use packaged fallback and reports that state truthfully.
10. Explicit project override wins only within that project.
11. Client A override/state is not visible in Client B's isolated profile.
12. Canonical repository content cannot install or execute behavior resources.

## Deadline guardrail

Do not let repository provisioning or live-sync polish block `TERMINAL_WORKSTATION_READY`. Implement against a fixture/temporary authorized remote if necessary, then bind the real canonical remote after owner provisioning and run the real-remote acceptance slice.
