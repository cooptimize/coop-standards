---
id: powerbi_semantic_model_tables
title: Organizing Power BI Tables
domain: powerbi
layer: semantic_model
artifact: table
technology: power_bi
status: active
---
# Organizing Tables

## Naming

- Use PascalCase table and calculated-column names.
- Column references MUST include the table name: `Table[Column]`.

## Fields

- Disable summarization for numeric columns not intended for aggregation.
- Format dates as `mm/dd/yyyy`.
- Display Boolean/BIT fields as `TRUE` / `FALSE`.
- Convert date/time values to the client's primary time zone in SQL, not with a fixed UTC offset.
- Display date/time values with the local date, time, and time-zone context, such as `10/06/2025 3:00 PM Eastern`.
- Include the time zone in the converted column name, such as `Created Date ET`.

## Date table

- Time intelligence MUST use one contiguous marked Date table.
- Disable Power BI auto date/time. Remove `LocalDateTable_*` and `DateTableTemplate_*` tables.
- Use `Calendar`, `Fiscal`, and `Relative` display folders when those fields exist.

## Dimension folders

Dimension display folders are optional. When used, organize fields into logical subject groups.

## Hierarchies and sorting

- Put ordered levels in a hierarchy.
- A hierarchy MAY use any clear name.
- Place first the field whose label can represent the hierarchy when a visual cannot rename it.
- Sort Date-table strings by an integer or Date column.
- Hide columns used only for sorting.

## Deployment

- Direct Lake models MUST NOT contain unsupported calculated columns.
- Direct Lake source table names MUST match the source exactly.
- Deploy semantic-model source with TMDL, not TMSL.
