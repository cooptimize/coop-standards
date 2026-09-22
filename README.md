# Cooptimize Standards

**Agents:** Read [AGENTS.md](AGENTS.md) before editing this repository.

This library defines how Cooptimize builds and reviews SQL and Power BI solutions. It gives developers, reviewers, and COOP one approved source for naming, structure, formatting, and design decisions.

These articles describe expected output, not step-by-step implementation patterns. Client requirements and approved project standards override this library within that project. Incremental loading and general performance guidance live in separate knowledge bases.

## SQL

### General

- [Formatting](sql/formatting.md)

### Silver

- [Deterministic generation](sql/silver/deterministic-generation.md)

### Gold

- [Dimension tables](sql/gold/dimension-tables.md)
- [Fact tables](sql/gold/fact-tables.md)
- [Stored procedures](sql/gold/stored-procedures.md)
- [Views](sql/gold/views.md)

### Technology

- [Fabric Warehouse](tech/fabric/warehouse.md)

## Power BI

### General

- [Choosing PBIX, PBIP, and PBIR](powerbi/file-types.md)

### Semantic models

- [M Query](powerbi/semantic-model/m-query.md)
- [Tables](powerbi/semantic-model/tables.md)
- [Fact measure and attribute tables](powerbi/semantic-model/fact-tables.md)
- [Relationships](powerbi/semantic-model/relationships.md)
- [Measures](powerbi/semantic-model/measures.md)
- [DAX](powerbi/semantic-model/dax.md)
- [Composite models](powerbi/semantic-model/composite-models.md)

### Reports

- [Visuals](powerbi/reports/visuals.md)

## Repository

- [Deterministic retrieval routes](standards.yml)
- [Deprecated standards](deprecation/)
