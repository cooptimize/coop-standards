---
id: powerbi_semantic_model_fact_tables
title: Power BI Fact Tables
domain: powerbi
layer: semantic_model
artifact: fact_table
technology: power_bi
status: active
---
# Fact Measure and Attribute Tables

## Table structure

- A fact with report-facing attributes MUST use a source-backed `{Fact Table} Attributes` table and a paired one-row `{Fact Table}` measure host.
- Report-facing fields MUST remain in the Attributes table and measures in the measure host. For example, use `Ledger Transaction Attributes` and `Ledger Transactions`.
- A fact without report-facing attributes MAY remain one source-backed table and MAY be split later when attributes are added.

## Display folders

Use these folders when the corresponding fields exist:

- `Attributes`
- `Keys`; hide every field in this folder.
- `Numbers`; hide every field in this folder.
