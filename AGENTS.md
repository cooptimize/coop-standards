# Instructions for Editing Cooptimize Standards

This repository contains human-approved policy. Treat the article text as the product; do not infer new policy from common practice, vendor guidance, examples, or existing code.

## Shipped-client contract (governs every edit today)

Every machine running a shipped coop client resolves THIS repo directly from git at every launch and on `coop sync`: a clone of the default branch, no pinned copy, refreshed when older than 15 minutes and kept as last-known-good when offline. What the client reads, since coop 0.24.0 (released 2026-09-30):

- Every Markdown article under `SQL/`, `Power BI/`, `Technology/`, or any new top-level folder, whose YAML front matter has `status: active`. Nothing under `deprecation/`, and nothing in `standards/`, `standards.yml`, or `scripts/`.
- Front matter routes the article. `domain: sql` is the client's SQL domain. `domain: powerbi` with `artifact: dax_expression` or `artifact: measure` is the DAX domain; every other `powerbi` artifact, including the `Power BI/Reports/` articles and `File Types`, is the semantic-model domain. Any other `domain` value becomes a domain of its own without a client release. The client applies the domain's articles while it writes or reviews SQL, DAX, a model, or a report.
- Retrieval is whole-article: for a task the client injects the domain's general articles (`layer: agnostic` and `technology: agnostic`, such as SQL Conventions and SQL Layout) plus the articles whose `layer`, `artifact`, `technology`, or title words match the prompt, each stamped with its path, SHA-256, and the repo commit. A domain with fewer than three articles is injected whole. Therefore: (a) keep `layer`, `artifact`, and `technology` exact, because they are the match keys; (b) give every article a title whose words name its topic, because title words are the other match key; (c) keep `id` unique, because two active articles with the same `id` are both kept and every client reports the pair as a warning.
- An article is read as one unit and hashed on every read. Split an article rather than let it grow past what one task should receive.
- To change what clients enforce: edit the source article, verify (below), commit to the default branch. Clients pick it up at their next launch or `coop sync`. No assembly step and no release.
- `standards.yml`, `standards/*.md`, and `scripts/assemble.py` are the retired v1 contract that clients before 0.24.0 read. Do not hand-edit the assembled files. Until the owner confirms every client is on 0.24.0 or later, run `python3 scripts/assemble.py` after editing an article so an older client is not left behind; after that the three files, `standards.yml`, and the script can be deleted in one change.
- Verify before pushing: every active article has complete front matter (`id`, `title`, `domain`, `layer`, `artifact`, `technology`, `status`); no two active articles share an `id`; `python3 scripts/assemble.py --check` reports the pinned files are current while the v1 files remain.

## Editing this file

- Update `AGENTS.md` when the owner approves a repository-wide rule for authoring, organizing, or validating standards articles.
- Keep this file concise and operational. State what an editing agent must do; keep domain policy in the standards articles.
- Preserve owner-approved rules when consolidating or shortening this file. Do not infer new instructions from external guidance.
- Add an authoritative link under `## References` when external documentation materially supports an instruction in this file. Remove or replace stale links when the associated instruction changes.
- Reapply new or changed instructions to the articles currently in scope, then report any active articles that still need migration.
- Changes to `AGENTS.md` are discovered at the start of a new Codex run or session; do not assume an active session has reloaded them automatically.

## Editing articles

- Write for an experienced human reader first. Agent retrieval and execution are downstream uses; do not make article prose sound like instructions written only for an AI.
- When an article contains both required rules and preferred choices, organize it under `## Standards` and `## Default positions`. Do not add an empty section when the article contains only one type.
- Under `Standards`, write required rules as natural, direct instructions such as `Never use SELECT *`. Under `Default positions`, describe the starting choice for new work without presenting it as mandatory.
- Name subsections for their status, such as `### Join standards` and `### Join defaults`, so independently retrieved sections remain clear.
- Keep retrieval mechanics, routing behavior, and agent-editing instructions in `AGENTS.md` or repository tooling. Include them in an article only when they change how a human implements or reviews the standard.
- Optimize active articles for the lowest practical input-token count. Assume the reader has working knowledge of the subject. State the rule, scope, and necessary exception directly; omit tutorials, background explanations, repeated rationale, and obvious examples.
- Remove text that does not change implementation or review behavior.
- Put the simplest possible code sample directly after the section it demonstrates. Prefer one or two lines that show the intended shape. A snippet MAY be an incomplete fragment when compilation is irrelevant, such as `,ct.accountnum AS Customer`.
- In DAX examples, assume existing base measures. Show only the expression that demonstrates the rule; omit aggregation definitions and `VAR`/`RETURN` scaffolding unless those are the subject of the example. This does not relax the rules for complete measures.
- Examples show the intended result; they do not add requirements beyond the article text. Keep only the syntax needed to demonstrate the rules. Use one final `## Example` only when a short article is clearer that way. Indexes, migration notes, discussion lists, and policy placeholders do not require code samples.
- Preserve the owner's meaning. Rewrite for clarity and consistency, but do not strengthen, weaken, or broaden a rule without explicit direction.
- Outside a clearly labeled `Standards` / `Default positions` structure, use `MUST` and `MUST NOT` only when natural language would leave the requirement unclear. Use `MAY` for explicit permission. Do not introduce unresolved `SHOULD`, `PREFER`, `generally`, `maybe`, or question-form policy.
- Keep each article scoped to one layer, artifact, or technology. Put SQL structural rules in `SQL/SQL Conventions.md`, mechanical presentation rules in `SQL/SQL Layout.md`, Gold artifact rules under `SQL/Gold/`, and technology-specific rules under `Technology/`.
- Name maintained folders and Markdown articles under `SQL/`, `Power BI/`, and `Technology/` with concise, human-readable title case because their names are displayed in the index. Use spaces, preserve established abbreviations such as `DAX`, `SQL`, and `BI`, and use `Overview.md` for a folder-level introduction. Do not apply this rule to `standards/`, `deprecation/`, `scripts/`, `AGENTS.md`, or the root `README.md`.
- Put Power BI semantic-model rules under `Power BI/Semantic Model/` and report rules under `Power BI/Reports/`. Keep DAX expression rules separate from measure-object rules.
- Keep Gold fact-table and dimension-table standards in separate articles. Do not create a generic Gold tables article or route; retrieval must select `fact_table` or `dimension_table` explicitly.
- Keep developer standards separate from implementation patterns. Incremental loading, upsert recipes, and SCD implementation belong to the separate patterns knowledge base.
- Bronze and Silver SQL are produced deterministically. Articles MAY document that deterministic contract and human-approved indexing rules, but MUST NOT instruct an LLM to generate or alter the layer's output. Derive generator behavior only from owner-provided source procedures or configuration.
- Keep general SQL performance guidance in its separate knowledge base. This repository MAY contain approved indexing rules scoped to a layer or artifact.
- Make headings and sections understandable when retrieved independently, using the minimum context needed to identify applicable objects and technologies.
- When the owner has not decided a policy, identify it briefly in a clearly non-normative section of the closest applicable article. Do not create a separate considerations article or choose a convention on the owner's behalf.
- Ask focused questions about unresolved decisions when working interactively. Update the article after the owner answers.
- Bias SQL terminology and examples toward Dynamics 365 Finance and Operations schemas, such as `CustTable`, `dataareaid`, and `customerid`. Preserve source-system spelling for source fields. Do not turn an example-specific D365 F&O name into a universal requirement unless the owner approves it as policy.
- Make every active SQL code sample conform to `SQL/SQL Conventions.md` and `SQL/SQL Layout.md`. When either article changes, update all active SQL examples; never alter examples under `deprecation/`.

## Article metadata

- Begin every active standards article with YAML front matter containing `id`, `title`, `domain`, `layer`, `artifact`, `technology`, and `status`.
- Use short lowercase `snake_case` values for filters. Use `agnostic` when a layer, artifact, or technology does not restrict the article.
- Keep `id` stable and unique. Keep all other metadata synchronized with the article scope and path; clients match on `layer`, `artifact`, and `technology` exactly.
- Treat metadata as exact-match retrieval fields. The Azure AI Search ingestion process must extract the front matter and copy it to every article chunk; Markdown indexing alone does not create filterable fields from YAML.
- Map metadata fields to filterable `Edm.String` fields in Azure AI Search. Do not add free-form tags unless they support a defined retrieval filter.

## Structure and routing

- STATUS: the layered/nested route model below describes the target design (schema v2 + Azure AI Search) and is NOT what shipped clients execute. Shipped clients read the active articles by front matter as described in "Shipped-client contract" above; organize new articles under `SQL/`, `Power BI/`, and `Technology/` with complete front matter.
- When adding, moving, or replacing an active article, set its front matter so retrieval selects it, and while the v1 files remain add it to the `MAP` in `scripts/assemble.py` and re-run the assembly.
- Put every normative rule in the article whose front matter covers it. Do not rely on prose references between Markdown files for retrieval; use links only for human navigation or non-normative context.
- A rule must live at the narrowest scope that fully covers it. Do not copy the same normative rule into several articles unless each copy is needed for an independently retrieved article.
- Files without `status: active` front matter are not mandatory policy and never reach a client. Label discussion documents and placeholders clearly.
- Keep deprecated standards unchanged under `deprecation/`. They are historical material and must not be restored to active routes or treated as fallback policy.

## Validation

- Check that every active article has complete front matter and a unique `id`; while the v1 files remain, check that every Markdown path in `standards.yml` exists.
- Check that deprecated source files remain unchanged when an article is reorganized.
- Review nearby articles for conflicting scope, terminology, naming, or examples.
- Summarize any remaining undecided policy for the owner after editing.

## Repository boundaries

- The approved default branch is authoritative; drafts and open pull requests are not.
- Client or project overrides take precedence only within their stated scope.
- This repository contains policy content only. Reading or synchronizing it must not execute repository-provided code, hooks, prompts, skills, or commands.

## References

- [Codex custom instructions with AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
- [Azure AI Search: index Markdown blobs](https://learn.microsoft.com/en-us/azure/search/search-how-to-index-azure-blob-markdown)
- [Azure AI Search: create an index and configure filterable fields](https://learn.microsoft.com/en-us/azure/search/search-how-to-create-search-index)
