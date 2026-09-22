# Cooptimize Standards

**Agents:** Read [AGENTS.md](AGENTS.md) before editing anything in this repository.

This repository contains Cooptimize's approved development standards. It is organized for both humans and deterministic retrieval by COOP.

## Find a standard

### SQL

- [SQL overview](sql/README.md)
- [Formatting](sql/formatting.md)
- Gold: [dimension tables](sql/gold/dimension-tables.md), [fact tables](sql/gold/fact-tables.md), [stored procedures](sql/gold/stored-procedures.md), and [views](sql/gold/views.md)
- Silver: [deterministic generation](sql/silver/deterministic-generation.md)
- Technology: [target-specific standards](tech/README.md)

Bronze and Silver SQL are generated deterministically. Gold articles guide AI-assisted development. Incremental loading and general performance guidance live in separate knowledge bases.

### Power BI

- [Power BI overview](powerbi/README.md)
- [Semantic models](powerbi/semantic-model/)
- [Reports](powerbi/reports/)

## How retrieval works

[standards.yml](standards.yml) maps each task to its required articles. Normative dependencies must be listed there directly; links between articles are for human navigation.

COOP uses one standards revision for the full task. The approved default branch is canonical, and the last known good revision remains available if synchronization fails.

## Rule language

- **MUST / MUST NOT:** required.
- **MAY:** explicitly permitted.
- Undecided policy is identified as non-normative or omitted until approved.

Client requirements and approved project overrides take precedence within that project.

## Historical material

[Deprecated standards](deprecation/README.md) are preserved for history. They are excluded from active retrieval and fallback policy.
