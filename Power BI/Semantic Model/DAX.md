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

## DAX structure standards

- Use consistent, readable formatting; DAX Formatter is allowed.
- Qualify columns as `Table[Column]`; leave measure references unqualified.
- A single aggregation or measure reference can remain one expression. Other measures use named `VAR` steps and `RETURN`.
- Use descriptive camel case variables without prefixes.
- Put intermediate results in variables; do not nest `CALCULATE` inside `CALCULATE`.
- Name business-meaningful numeric and string constants with variables. Arithmetic `0`, `1`, and `100`, plus `BLANK()`, `TRUE()`, and `FALSE()`, can stay inline.

```dax
VAR result = [Sales Amount] - [Sales Cost]
RETURN result
```

## DAX average standards

Never use `AVERAGE` or `AVERAGEX`. Explicitly define the business numerator and denominator, then use `DIVIDE`.

```dax
VAR numerator = SUM(FactSales[Revenue])
VAR denominator = SUM(FactSales[Quantity])
VAR result = DIVIDE(numerator, denominator)
RETURN result
```

## CALCULATE filter standards

Use `CALCULATE` to change a report selection or use a different relationship. The fragments below illustrate filtering; complete measures still follow the variable rules above.

### CALCULATE replacing a selection

The report selects **Blue**. A direct **Red** predicate replaces Blue and returns Red sales.

```dax
CALCULATE([Sales Amount], Product[Color] = "Red")
```

### CALCULATE keeping both selections

The report selects **Blue**. `KEEPFILTERS` also requires **Red**, so there are no matching products and a SUM-based measure returns blank.

```dax
CALCULATE([Sales Amount], KEEPFILTERS(Product[Color] = "Red"))
```

### CALCULATE filtering visible values

The report selects **Blue**. `VALUES` contains only Blue, so filtering it for Red returns no matches.

```dax
CALCULATE([Sales Amount], FILTER(VALUES(Product[Color]), Product[Color] = "Red"))
```

Use `FILTER` to test visible groups, evaluate a measure, or compare fields. For example, retain only visible months with profit:

```dax
CALCULATE([Sales Amount], FILTER(VALUES('Date'[Month]), [Sales Profit] > 0))
```

Do not treat `FILTER` and `Field = value` as interchangeable. Empty results produce blank for a SUM-based measure; zero requires the base measure or another expression to produce zero.

### CALCULATE removing selections

`ALL(Color)` removes the Color selection and keeps selections on other fields. With Blue selected, this returns all colors:

```dax
CALCULATE([Sales Amount], ALL(Product[Color]))
```

`ALLEXCEPT` keeps Brand and removes other Product selections. Use it only when ignoring every other selection on that table is intentional.

```dax
CALCULATE([Sales Amount], ALLEXCEPT(Product, Product[Brand]))
```

### CALCULATE relationship selection

Use `USERELATIONSHIP` to calculate through the specified relationship.

```dax
CALCULATE([Sales Amount], USERELATIONSHIP(FactSales[FKShipDate], 'Date'[PKDate]))
```

## DAX grouping standards

- Use `SUMMARIZE` for a grouped table built from a specific table or filtered table variable.
- Use `SUMMARIZECOLUMNS` for standalone queries returning grouped model fields and measures.
- Use `VALUES(Column)` for one distinct field.
- Group only at the level required by the business calculation.

```dax
VAR salesByOrder = SUMMARIZE(FactSales, FactSales[SalesOrder], "salesAmount", [Sales Amount])
```

```dax
EVALUATE
SUMMARIZECOLUMNS('Date'[FiscalYear], Customer[CustomerGroup], "salesAmount", [Sales Amount])
```

## DAX total standards

Test detail rows, subtotals, and grand totals separately. Power BI recalculates the total; it does not automatically add displayed rows.

When the business definition requires adding row results, define the grouping explicitly and iterate over it.

```dax
VAR result = SUMX(salesByOrder, [salesAmount])
RETURN result
```

## DAX function standards

- Use `DIVIDE` instead of `/`.
- Replace `EARLIER` and `EARLIEST` with a variable holding the outer-row value.
- Do not wrap arithmetic in `IFERROR`. Use `DIVIDE` or explicit tests for expected blanks.

```dax
DIVIDE([Sales Amount], [Sales Quantity])
```

## Complex DAX review standards

Before adding more complex DAX, check what one source row represents, the relationships, and source transformations. When the model structure causes the complexity, move stable joins and row-level business transformations into the model or source layer.

## References (non-normative)


- [Microsoft DAX `VAR` syntax and identifier rules](https://learn.microsoft.com/en-us/dax/var-dax)
- [Microsoft: avoid using `FILTER` as a `CALCULATE` filter argument](https://learn.microsoft.com/en-us/dax/best-practices/dax-avoid-avoid-filter-as-filter-argument)
- [Microsoft `KEEPFILTERS` behavior](https://learn.microsoft.com/en-us/dax/keepfilters-function-dax)
- [Microsoft `AVERAGE` behavior](https://learn.microsoft.com/en-us/dax/average-function-dax)
- [Microsoft `SUMMARIZE`](https://learn.microsoft.com/en-us/dax/summarize-function-dax)
- [Microsoft `SUMMARIZECOLUMNS`](https://learn.microsoft.com/en-us/dax/summarizecolumns-function-dax)
- [Microsoft `ALL`](https://learn.microsoft.com/en-us/dax/all-function-dax)
- [Microsoft `ALLEXCEPT`](https://learn.microsoft.com/en-us/dax/allexcept-function-dax)
