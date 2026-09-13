# Cooptimize Standards

Canonical formal standards consumed by COOP.

## Files

- `standards/sql.md` — SQL authoring and Fabric Warehouse rules.
- `standards/dax.md` — DAX expression and measure-authoring rules.
- `standards/semantic-model.md` — Power BI semantic-model structure, organization, formatting, and composite-model rules.

## Authority

These files are Cooptimize defaults. Effective precedence is:

1. Explicit client requirement or approved project override.
2. Canonical Cooptimize standard from the approved default branch of this repository.
3. Last-known-good canonical revision when the remote is temporarily unavailable.
4. Bundled COOP reviewer fallback when no canonical revision has ever been synchronized.

A project override applies only to that project. It does not modify this repository.

## Directive language

- `MUST` / `MUST NOT` — required policy.
- `MAY` — explicitly permitted behavior.

Canonical policy does not use unresolved `SHOULD`, `PREFER`, `generally`, `maybe`, or `...?` language. Unsettled policy is omitted until approved.

## Live-policy behavior

The approved default branch is the authoritative policy stream. Draft branches and open pull requests are not authoritative.

COOP must:

- synchronize the canonical default branch automatically at startup when online;
- re-check freshness before a standards-governed task when the last successful remote check is more than 15 minutes old;
- make `coop sync` force an immediate standards refresh;
- keep the last-known-good revision if refresh fails;
- invalidate the standards retrieval index/cache when the canonical revision changes;
- pin one exact standards commit for the duration of a task so generation and deterministic review use the same revision; and
- expose the source repository, commit, effective file, and fallback state in diagnostics/provenance.

A merged standards change therefore becomes available to isolated client COOP installations without reinstalling COOP. A task already in progress finishes against the revision it started with; the next task uses the newly synchronized revision.

## Security boundary

This repository is policy content only. Synchronizing or reading it must never execute repository-provided scripts, hooks, binaries, prompts, skills, or arbitrary commands.

## Change control

Standards changes are reviewed as standards changes. TeamAI learnings and Incremental BI patterns do not automatically modify these files.
