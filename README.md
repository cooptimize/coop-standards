# Cooptimize Standards

**Agents:** Read [AGENTS.md](AGENTS.md) before editing this repository.

This library defines how Cooptimize builds and reviews SQL and Power BI solutions. It gives developers, reviewers, and COOP one approved source for naming, structure, formatting, and design decisions.

These articles describe expected output, not step-by-step implementation patterns. Client requirements and approved project standards override this library within that project. Incremental loading and general performance guidance live in separate knowledge bases.

## SQL

### General

- [SQL Formatting](<sql/SQL Formatting.md>)

### Silver

- [Overview](sql/silver/Overview.md)

### Gold

- [Dimension Tables](<sql/gold/Dimension Tables.md>)
- [Fact Tables](<sql/gold/Fact Tables.md>)
- [Stored Procedures](<sql/gold/Stored Procedures.md>)
- [Views](sql/gold/Views.md)

### Technology

- [Fabric Warehouse](<tech/fabric/Fabric Warehouse.md>)

## Power BI

### General

- [File Types](<powerbi/File Types.md>)

### Semantic models

- [M Query](<powerbi/semantic-model/M Query.md>)
- [Tables](powerbi/semantic-model/Tables.md)
- [Fact Tables](<powerbi/semantic-model/Fact Tables.md>)
- [Relationships](powerbi/semantic-model/Relationships.md)
- [Measures](powerbi/semantic-model/Measures.md)
- [DAX](powerbi/semantic-model/DAX.md)
- [Composite Models](<powerbi/semantic-model/Composite Models.md>)

### Reports

- [Visuals](powerbi/reports/Visuals.md)

## Repository

- [Deterministic retrieval routes](standards.yml)
- [Deprecated standards](deprecation/)
