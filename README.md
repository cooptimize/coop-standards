# Cooptimize Standards

**Agents:** Read [AGENTS.md](AGENTS.md) before editing this repository.

This library defines how Cooptimize builds and reviews SQL and Power BI solutions. It gives developers, reviewers, and COOP one approved source for naming, structure, formatting, and design decisions.

These articles describe expected output, not step-by-step implementation patterns. Client requirements and approved project standards override this library within that project. Incremental loading and general performance guidance live in separate knowledge bases.

## SQL

### General

- [SQL Conventions](<SQL/SQL Conventions.md>)
- [SQL Layout](<SQL/SQL Layout.md>)

### Silver

- [Overview](SQL/Silver/Overview.md)

### Gold

- [Dimension Tables](<SQL/Gold/Dimension Tables.md>)
- [Fact Tables](<SQL/Gold/Fact Tables.md>)
- [Stored Procedures](<SQL/Gold/Stored Procedures.md>)
- [Views](SQL/Gold/Views.md)

### Technology

- [Fabric Warehouse](<Technology/Fabric/Fabric Warehouse.md>)

## Power BI

### General

- [File Types](<Power BI/File Types.md>)

### Semantic models

- [M Query](<Power BI/Semantic Model/M Query.md>)
- [Organizing Tables](<Power BI/Semantic Model/Organizing Tables.md>)
- [Fact Tables](<Power BI/Semantic Model/Fact Tables.md>)
- [Relationships](<Power BI/Semantic Model/Relationships.md>)
- [Measures](<Power BI/Semantic Model/Measures.md>)
- [DAX](<Power BI/Semantic Model/DAX.md>)
- [Composite Models](<Power BI/Semantic Model/Composite Models.md>)

### Reports

- [App Deployment](<Power BI/Reports/App Deployment.md>)
- [Page Formatting](<Power BI/Reports/Page Formatting.md>)
- [Visuals](<Power BI/Reports/Visuals.md>)

## Repository

- [Deterministic retrieval routes](standards.yml)
- [Deprecated standards](deprecation/)
