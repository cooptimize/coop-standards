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

## Fact table structure standards

- A fact with report-facing attributes uses a source-backed Attributes table and a paired one-row measure table named for the fact.
- Keep fields in Attributes and measures in the measure table.
- A fact without report-facing attributes can remain one source-backed table and be split later.

| Table | Contents |
|---|---|
| Ledger Transaction Attributes | Source rows and fields |
| Ledger Transactions | One-row table holding measures |

## Calculation table standards

- Put measures associated with one fact in its measure table.
- Every model includes `Ad Hoc Calculations` for measures authored inside reports, primarily for testing.
- Put measures spanning facts that do not belong to a single fact's measure table in `Multi-Fact Calculations`.
- Hide the technical `Calculation` field in every measure table.

## Fact display-folder standards

Use these folders when the fields exist:

| Folder | Visibility |
|---|---|
| Attributes | Report-facing fields |
| Keys | All fields hidden |
| Numbers | All fields hidden |

## Open decisions (non-normative)

- A universal singular/plural naming rule is not defined; `Ledger Transaction Attributes` and `Ledger Transactions` are the approved example.
- Whether one-row measure tables must remain disconnected is not explicitly defined. Do not infer a relationship requirement from the phrase "one-row table."
