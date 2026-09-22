---
id: powerbi_semantic_model_dax
title: Power BI DAX
domain: powerbi
layer: semantic_model
artifact: dax_expression
technology: power_bi
status: active
---
# DAX

## Naming and structure

- DAX MUST use consistent, readable formatting. DAX Formatter MAY be used.
- Qualify columns as `Table[Column]`; do not qualify measure references.
- A single aggregation or measure reference MAY remain one expression.
- Every other measure MUST use named `VAR` steps and `RETURN`.
- Variable names MUST use descriptive lower camel case, such as `largeOrders` and `result`. They MUST NOT use a prefix.
- Split intermediate results into variables; do not nest `CALCULATE` inside `CALCULATE`.
- Declare business-meaningful numeric and string literals as named variables. Arithmetic `0`, `1`, and `100`, plus `BLANK()`, `TRUE()`, and `FALSE()`, MAY remain inline.

## Local filters

When filtering fact rows without changing report selections:

- isolate the filtered rows in a table variable;
- aggregate with an explicit iterator such as `SUMX`, `COUNTX`, `MINX`, or `MAXX`; and
- do not use `CALCULATE`.

```dax
VAR largeOrderQuantityThreshold = 10
VAR largeOrders =
    FILTER(
        FactSales,
        FactSales[Quantity] > largeOrderQuantityThreshold
    )
VAR result =
    SUMX(largeOrders, FactSales[Revenue])
RETURN
    result
```

## Averages

- `AVERAGE()` and `AVERAGEX()` MUST NOT be used because their denominators are implicit.
- Define the business numerator and denominator separately, then use `DIVIDE()`.

```dax
VAR numerator = SUM(FactSales[Revenue])
VAR denominator = SUM(FactSales[Quantity])
VAR result = DIVIDE(numerator, denominator)
RETURN
    result
```

## CALCULATE

Use `CALCULATE` when the measure must change a report selection or use a different relationship.

The next three examples assume the report is filtered to Blue and the measure asks for Red.

### Replace a selection

If the report selects Blue, this expression ignores that selection and returns Red revenue:

```dax
CALCULATE(
    [Sales Amount],
    Product[Color] = "Red"
)
```

### Require both selections

If the report selects Blue, this expression returns blank because a product cannot be both Blue and Red:

```dax
CALCULATE(
    [Sales Amount],
    KEEPFILTERS(Product[Color] = "Red")
)
```

Use `KEEPFILTERS` when the calculation must honor the report selection and add another requirement to the same field.

### Filter visible groups

`FILTER(VALUES(...))` searches only the values visible in the report. Because only Blue is visible, it cannot find Red and returns `BLANK()`:

```dax
CALCULATE(
    [Sales Amount],
    FILTER(
        VALUES(Product[Color]),
        Product[Color] = "Red"
    )
)
```

Use `FILTER` when the rule must test each visible group, evaluate a measure, or compare fields. This example keeps only visible months with profit:

```dax
CALCULATE(
    [Sales Amount],
    FILTER(
        VALUES('Date'[Month]),
        [Sales Profit] > 0
    )
)
```

`FILTER` and `Field = value` MUST NOT be treated as equivalent. Use `Field = value` to replace the report selection, `KEEPFILTERS(Field = value)` to require both values, and `FILTER(VALUES(Field), ...)` to search only visible values. A `SUM`-based measure returns `BLANK()` for the empty result; it returns zero only when the base measure or another expression produces zero.

### Remove selections

`ALL(Product[Color])` removes only the Color selection. If the report selects Blue, this returns sales for all colors while retaining selections on other fields:

```dax
CALCULATE(
    [Sales Amount],
    ALL(Product[Color])
)
```

`ALLEXCEPT(Product, Product[Brand])` removes every selection on Product except Brand. If the report selects Brand and Color, this retains Brand and returns sales for all colors and other product fields:

```dax
CALCULATE(
    [Sales Amount],
    ALLEXCEPT(Product, Product[Brand])
)
```

Use `ALLEXCEPT` only when every other selection on that table is intentionally ignored.

### Use a different relationship

```dax
CALCULATE(
    [Sales Amount],
    USERELATIONSHIP(FactSales[FKShipDate], 'Date'[PKDate])
)
```

## Measures inside iterators

- A measure called inside an iterator evaluates for that iterator's current row.
- When this row-specific behavior is required, add a nearby comment explaining why.
- Do not use this behavior as an implicit lookup over duplicate rows.

## SUMMARIZE and SUMMARIZECOLUMNS

- Use `SUMMARIZE` when a measure needs a grouped table built from a specific table or previously filtered table variable.
- Use `SUMMARIZECOLUMNS` for a standalone DAX query that returns grouped model fields and measures.
- Use `VALUES(Column)` when only one distinct field is required.
- Group only at the business grain required by the calculation.

```dax
VAR salesByOrder =
    SUMMARIZE(
        FactSales,
        FactSales[SalesOrder],
        "salesAmount", [Sales Amount]
    )
VAR result =
    SUMX(salesByOrder, [salesAmount])
RETURN
    result
```

```dax
EVALUATE
SUMMARIZECOLUMNS(
    'Date'[FiscalYear],
    Customer[CustomerGroup],
    "salesAmount", [Sales Amount]
)
```

## Totals

- Validate detail rows, subtotals, and grand totals separately. Power BI recalculates a total for the whole total row; it does not automatically add the visible rows above it.
- When the business definition requires summing row-level results, define the required grain explicitly and use an iterator over that grain.

## Functions

- Use `DIVIDE()` instead of `/`.
- Do not use `EARLIER` or `EARLIEST`; capture the outer-row value in a variable.
- Do not wrap arithmetic in `IFERROR`; use `DIVIDE()` or explicit tests for expected blank conditions.

## Model-first review

Complex DAX MUST trigger a review of the underlying table grain, relationships, and source transformations before more logic is added. Stable joins and row-level business transformations belong in the model or source layer when the complexity is caused by model structure.

## References (non-normative)

- [Microsoft DAX `VAR` syntax and identifier rules](https://learn.microsoft.com/en-us/dax/var-dax)
- [Microsoft: avoid using `FILTER` as a `CALCULATE` filter argument](https://learn.microsoft.com/en-us/dax/best-practices/dax-avoid-avoid-filter-as-filter-argument)
- [Microsoft `KEEPFILTERS` behavior](https://learn.microsoft.com/en-us/dax/keepfilters-function-dax)
- [Microsoft `AVERAGE` behavior](https://learn.microsoft.com/en-us/dax/average-function-dax)
- [Microsoft `SUMMARIZE`](https://learn.microsoft.com/en-us/dax/summarize-function-dax)
- [Microsoft `SUMMARIZECOLUMNS`](https://learn.microsoft.com/en-us/dax/summarizecolumns-function-dax)
- [Microsoft `ALL`](https://learn.microsoft.com/en-us/dax/all-function-dax)
- [Microsoft `ALLEXCEPT`](https://learn.microsoft.com/en-us/dax/allexcept-function-dax)
