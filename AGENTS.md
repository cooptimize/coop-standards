# Instructions for Editing Cooptimize Standards

This repository contains human-approved policy. Treat the article text as the product; do not infer new policy from common practice, vendor guidance, examples, or existing code.

## Editing this file

- Update `AGENTS.md` when the owner approves a repository-wide rule for authoring, organizing, or validating standards articles.
- Keep this file concise and operational. State what an editing agent must do; keep domain policy in the standards articles.
- Preserve owner-approved rules when consolidating or shortening this file. Do not infer new instructions from external guidance.
- Add an authoritative link under `## References` when external documentation materially supports an instruction in this file. Remove or replace stale links when the associated instruction changes.
- Reapply new or changed instructions to the articles currently in scope, then report any active articles that still need migration.
- Changes to `AGENTS.md` are discovered at the start of a new Codex run or session; do not assume an active session has reloaded them automatically.

## Editing articles

- Optimize active articles for the lowest practical input-token count. Assume the reader has working knowledge of the subject. State the rule, scope, and necessary exception directly; omit tutorials, background explanations, repeated rationale, and obvious examples.
- Remove text that does not change implementation or review behavior.
- Put the simplest possible code sample directly after the section it demonstrates. A short article MAY use one final `## Example`; otherwise use small local examples so each retrieved section is self-contained.
- Examples show the intended result; they do not add requirements beyond the article text. Keep only the syntax needed to demonstrate the rules. Indexes, migration notes, discussion lists, and policy placeholders do not require code samples.
- Preserve the owner's meaning. Rewrite for clarity and consistency, but do not strengthen, weaken, or broaden a rule without explicit direction.
- Use `MUST` and `MUST NOT` for requirements and `MAY` for explicit permission. Do not introduce unresolved `SHOULD`, `PREFER`, `generally`, `maybe`, or question-form policy.
- Keep each article scoped to one layer, artifact, or technology. Put SQL presentation and structural conventions in `sql/formatting.md`, Gold artifact rules under `sql/gold/`, and technology-specific rules under `tech/`.
- Put Power BI semantic-model rules under `powerbi/semantic-model/` and report rules under `powerbi/reports/`. Keep DAX expression rules separate from measure-object rules.
- Keep Gold fact-table and dimension-table standards in separate articles. Do not create a generic Gold tables article or route; retrieval must select `fact_table` or `dimension_table` explicitly.
- Keep developer standards separate from implementation patterns. Incremental loading, upsert recipes, and SCD implementation belong to the separate patterns knowledge base.
- Bronze and Silver SQL are produced deterministically. Articles MAY document that deterministic contract and human-approved indexing rules, but MUST NOT instruct an LLM to generate or alter the layer's output. Derive generator behavior only from owner-provided source procedures or configuration.
- Keep general SQL performance guidance in its separate knowledge base. This repository MAY contain approved indexing rules scoped to a layer or artifact.
- Make headings and sections understandable when retrieved independently, using the minimum context needed to identify applicable objects and technologies.
- When the owner has not decided a policy, identify it briefly in a clearly non-normative section of the closest applicable article. Do not create a separate considerations article or choose a convention on the owner's behalf.
- Ask focused questions about unresolved decisions when working interactively. Update the article after the owner answers.
- Bias SQL terminology and examples toward Dynamics 365 Finance and Operations schemas, such as `CustTable`, `dataareaid`, and `customerid`. Preserve source-system spelling for source fields. Do not turn an example-specific D365 F&O name into a universal requirement unless the owner approves it as policy.
- Make every active SQL code sample conform to `sql/formatting.md`. When that article changes, update all active SQL examples; never alter examples under `deprecation/`.

## Article metadata

- Begin every active standards article with YAML front matter containing `id`, `title`, `domain`, `layer`, `artifact`, `technology`, and `status`.
- Use short lowercase `snake_case` values for filters. Use `agnostic` when a layer, artifact, or technology does not restrict the article.
- Keep `id` stable and unique. Keep all other metadata synchronized with the article scope, path, and `standards.yml` route.
- Treat metadata as exact-match retrieval fields. The Azure AI Search ingestion process must extract the front matter and copy it to every article chunk; Markdown indexing alone does not create filterable fields from YAML.
- Map metadata fields to filterable `Edm.String` fields in Azure AI Search. Do not add free-form tags unless they support a defined retrieval filter.

## Structure and routing

- When adding, moving, or replacing an active article, update `standards.yml` so deterministic lookup selects the correct file.
- Put every normative article dependency directly in the applicable `standards.yml` route. Do not rely on prose references between Markdown files for retrieval; use links only for human navigation or non-normative context.
- A rule must live at the narrowest scope that fully covers it. Do not copy the same normative rule into several articles unless each copy is needed for an independently retrieved article.
- Files not listed in an active `standards.yml` route are not mandatory policy. Label discussion documents and placeholders clearly.
- Keep deprecated standards unchanged under `deprecation/`. They are historical material and must not be restored to active routes or treated as fallback policy.

## Validation

- Check that every Markdown path in `standards.yml` exists.
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
