# DAX Standards

Canonical Cooptimize DAX policy. Existing numbered section identities are preserved so current `coop-dax-review` references remain stable.

## Execution Model

- A measure that is a single aggregation or single measure reference MAY remain a single expression.
- Every other measure MUST use named `VAR` steps and `RETURN`.
- Routine local row filtering MUST use table variables plus explicit iterators.
- `CALCULATE` MAY be used only for the three cases defined in section 30.

## 1. Naming Conventions

- Measures MUST use `[Category: Name]`, for example `[Sales: Total Revenue]`.
- Calculated columns MUST use PascalCase.
- Tables MUST use PascalCase.
- Column references MUST include the table name: `Table[Column]`.
- Measure references MUST NOT include a table prefix: `[Measure Name]`.

## 2. VAR / RETURN Structure

A measure with more than one logical step MUST use `VAR` / `RETURN`. A single-expression core measure MAY omit `VAR` / `RETURN`.

## 3. No Nested CALCULATE

`CALCULATE` MUST NOT be nested inside another `CALCULATE`. Intermediate results MUST be split into variables.

## 4. CALCULATE Filter Arguments

When `CALCULATE` is justified under section 30:

- boolean column predicates MUST be used when they can express the filter;
- `FILTER(<table>, ...)` MUST NOT be passed as a filter argument when an equivalent boolean column predicate is sufficient; and
- a filter predicate that replaces an outer filter MUST be used only when replacement is intentional.

Routine local filtering that retains the existing report context is governed by section 28.

## 5. KEEPFILTERS

When a `CALCULATE` predicate must intersect with an existing filter on the same column instead of replacing it, the predicate MUST be wrapped in `KEEPFILTERS`.

## 6. Star Schema

Semantic models reviewed with these standards MUST use a star-schema shape unless an explicit client/project contract overrides it. Dimensions MUST be flat; relationship chains through intermediate dimension tables MUST NOT be introduced as the default model shape.

## 7. Bidirectional Relationships

Physical bidirectional relationships MUST NOT be the default. When a measure requires temporary bidirectional propagation, it MUST use targeted `CROSSFILTER` inside that measure unless an explicit project override requires a physical bidirectional relationship.

## 8. Marked Date Table

Time-intelligence logic MUST use one contiguous marked Date table.

## 9. Context Transition

- Context transition MUST NOT be relied on accidentally.
- A measure reference inside an iterator that intentionally causes row-to-filter context transition MUST be treated under sections 30 and 32.
- Context transition over a non-unique/duplicate-row table MUST NOT be used as an implicit lookup mechanism.

## 10. Measure Authoring Workflow

Before writing a measure, the author MUST establish:

1. the business definition and evaluation grain;
2. which report filters the result must respect or ignore; and
3. whether marked-Date-table logic is required.

Measure logic MUST be built and tested incrementally rather than expanded before the prior step is validated.

## 11. Measure Validation

Before a measure is accepted, validate:

- the unfiltered/base result;
- behavior with and without relevant slicers;
- blank, zero, and no-row cases; and
- a known control total when one exists.

## 13. Deployment Validation

- Direct Lake models MUST NOT introduce calculated columns where Direct Lake does not support them.
- Direct Lake source table names MUST match the source exactly.
- Semantic-model source intended for deployment MUST use TMDL rather than TMSL.

## 14. Division

Division MUST use `DIVIDE()` instead of `/`.

## 15. Measure Format Strings

Every visible measure MUST declare an explicit `formatString`.

## 16. Relationship Key Types

Relationship key columns MUST use exact numeric types such as `int64` or `decimal`. Relationship keys MUST NOT use floating-point `double`.

## 17. Hide Foreign Keys

Relationship key columns on the many side MUST be hidden from report view.

## 18. Key Summarization

Numeric relationship key columns MUST set `summarizeBy: none`.

## 20. Explicit Measures

Business aggregations MUST be exposed as explicit measures. Visible numeric columns that are not intended for direct aggregation MUST be hidden or set to `summarizeBy: none`.

## 21. Auto Date/Time

Power BI auto date/time MUST be disabled. `LocalDateTable_*` and `DateTableTemplate_*` auto-generated tables MUST NOT remain in the governed model.

## 22. EARLIER / EARLIEST

New DAX MUST NOT use `EARLIER` or `EARLIEST`. The required outer-row value MUST be captured in a variable before entering the inner row context.

## 23. Inactive Relationships

Every inactive relationship MUST be activated by at least one intentional `USERELATIONSHIP()` use. An inactive relationship with no consumer MUST be removed.

## 24. IFERROR

Arithmetic MUST NOT be wrapped in `IFERROR`. Use `DIVIDE()` for divide-by-zero handling and explicit input tests for expected blank conditions.

## 25. Measure Descriptions

Every visible measure MUST have a description. Hidden helper measures MAY omit descriptions.

## 27. Variable Names

Every local variable MUST use one leading underscore, for example `VAR _Result`.

## 28. Routine Local Filters

A routine local filter is a row/data predicate that does not intentionally replace report filter state, alter a relationship, or perform context transition.

For routine local filters:

- filtering MUST be isolated in a table variable;
- aggregation MUST use an explicit iterator such as `SUMX`, `COUNTX`, `AVERAGEX`, `MINX`, or `MAXX`; and
- `CALCULATE` MUST NOT be used.

```dax
VAR _LargeOrderQuantityThreshold = 10
VAR _LargeOrders =
    FILTER(
        FactSales,
        FactSales[Quantity] > _LargeOrderQuantityThreshold
    )
VAR _Result =
    SUMX(_LargeOrders, FactSales[Revenue])
RETURN
    _Result
```

## 29. No Gratuitous CALCULATE

`CALCULATE` MUST NOT wrap a scalar expression or aggregation when no filter-state, relationship/security, or context-transition behavior is required.

## 30. The Three Allowed CALCULATE Uses

`CALCULATE` MAY be used only for one or more of these purposes:

1. **Filter-state override** - deliberate manipulation of active visual/page/report filter state, including time-intelligence date-context replacement.
2. **Relationship/security override** - `USERELATIONSHIP`, `CROSSFILTER`, or another deliberate relationship/security propagation change.
3. **Deliberate context transition** - row-to-filter transition where the transition itself is required by the calculation.

If none applies, section 28 governs the filter/aggregation shape.

## 31. Business Literals

A numeric or string literal that carries business meaning MUST be declared as a named variable before use.

The literals `0`, `1`, and `100` MAY remain inline when they are used only for ordinary arithmetic. `BLANK()`, `TRUE()`, and `FALSE()` are not treated as business literals.

## 32. Intentional Context Transition

A measure reference or single-argument `CALCULATE` inside an iterator MUST NOT create an accidental context transition.

If per-row context transition is required:

- it MUST fall under section 30 case 3; and
- a nearby comment MUST state that the context transition is intentional.

## 26. References (Non-Normative)

- Microsoft Fabric Skills for GitHub Copilot: <https://github.com/microsoft/skills-for-fabric>
- Microsoft Fabric Semantic Model Authoring: <https://github.com/microsoft/skills-for-fabric/tree/main/skills/semantic-model-authoring>
- Microsoft Fabric DAX Guidelines: <https://github.com/microsoft/skills-for-fabric/tree/main/skills/semantic-model-authoring/references/dax-guidelines.md>
- Microsoft Fabric Direct Lake Guidelines: <https://github.com/microsoft/skills-for-fabric/tree/main/skills/semantic-model-authoring/references/direct-lake-guidelines.md>
- Greg Deckler, *DAX for Humans* (2025)
- SQLBI: <https://www.sqlbi.com>
