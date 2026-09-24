---
id: powerbi_semantic_model_tables
title: Organizing Power BI Tables
domain: powerbi
layer: semantic_model
artifact: table
technology: power_bi
status: active
---
# Organizing Semantic Model Tables

## Table naming standards

- Use PascalCase table and calculated-column names.
- Qualify column references with the table name.

```dax
Customer[CustomerGroup]
```

## Field formatting standards

- Disable summarization for numeric columns not intended for aggregation.
- Format dates as `mm/dd/yyyy` and Boolean/BIT fields as `TRUE` / `FALSE`.
- Convert timestamps to the client's primary time zone in SQL using time-zone conversion, never a fixed UTC offset.
- Show the local date, time, and zone; include the zone in the column name.

```text
Created Date ET: 10/06/2025 3:00 PM Eastern
```

## Date table standards

- Use one contiguous, marked Date table for time intelligence.
- Disable auto date/time and remove `LocalDateTable_*` and `DateTableTemplate_*` tables.
- Use `Calendar`, `Fiscal`, and `Relative` folders when those fields exist.

## Dimension folder standards

Dimension folders are optional. When used, group fields by subject.

## Hierarchy and sorting standards

- Put ordered levels in a hierarchy with a clear name.
- Put first the field whose label can represent the hierarchy in visuals where it cannot be renamed.
- Sort Date-table strings by an integer or Date column. Hide sort-only columns.

```text
Month Name → sort by Month Number (hidden)
```

## Semantic model deployment standards

- Do not use unsupported calculated columns in Direct Lake models.
- Direct Lake table names match their source exactly.
- Deploy semantic-model source with TMDL, not TMSL.

## Open decisions (non-normative)

Clarify the scope of PascalCase naming: approved measure-table names and report-facing column names contain spaces, and Direct Lake tables retain source names.
