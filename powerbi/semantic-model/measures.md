---
id: powerbi_semantic_model_measures
title: Power BI Measures
domain: powerbi
layer: semantic_model
artifact: measure
technology: power_bi
status: active
---
# Measures

## Naming and placement

- Name a base measure for the business value it returns, such as `[Sales Amount]` or `[Sales Quantity]`.
- Every model MUST contain an `Ad Hoc Calculations` table for report-authored measures.
- Put measures spanning more than one fact in `Multi-fact {Data Model Name} Measures`.
- Hide the technical `Calculation` field in measure tables.
- Name a filtered measure `{Base Measure} | {Filter}`, such as `[Sales Amount | Intercompany]`.
- A filtered measure MUST reference its base measure instead of duplicating the aggregation.

```dax
[Sales Amount | Intercompany] =
VAR result =
    CALCULATE(
        [Sales Amount],
        KEEPFILTERS(Customer[Intercompany] = TRUE())
    )
RETURN
    result
```

## Base measures

An additive base measure MUST use `SUM(Table[NumberField])`.

```dax
[Sales Amount] = SUM('Sales Transactions'[SalesAmount])
```

## SQL or DAX

Use this placement default:

- Default organization-certified calculations to Gold SQL when they are used, or are expected to be used, by multiple semantic models.
- Otherwise, implement the calculation in DAX. Model-specific filtered measures MUST remain DAX measures built from a base measure.

## Visibility and descriptions

- Expose business aggregations as explicit measures.
- Hide visible numeric columns not intended for direct aggregation or set them to `summarizeBy: none`.
- Every visible measure MUST have a description. Hidden helper measures MAY omit one.

## Formats

- Every visible measure MUST declare an explicit `formatString`.
- Whole numbers MUST default to `#,###`.
- Percentages MUST use `##%` unless a project-specific format overrides it.
- Currency MUST use `"$ #,0;–$ #,0;$ 0;--"` unless a project-specific format overrides it.
- Numeric-measure formats MUST align commas and decimal points within the visual.
- When parenthesized negative currency or percentage values require alignment, use a dynamic format with a non-breaking space and regular Segoe UI. Do not use an ordinary trailing space or bold/semibold variants.

```dax
"$ #,0" & UNICHAR(160) & ";$ (#,0);$ 0" & UNICHAR(160)
```

## Authoring and validation

Before authoring a measure, establish its business definition, evaluation grain, required filter behavior, and date-table requirements.

Build and test measure logic incrementally before expanding it.

Validate the base result, relevant slicers, blank/zero/no-row cases, and a known control total when available.
