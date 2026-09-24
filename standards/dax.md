<!-- ASSEMBLED from structured articles by scripts/assemble.py.
     Edit the source article under SQL/, Power BI/, or Technology/ and re-run
     `python3 scripts/assemble.py`. Do not hand-edit sections here. -->

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

Never use `AVERAGE` or `AVERAGEX`: they leave the business numerator and denominator implied, making the intended average ambiguous. Define both explicitly, then use `DIVIDE` so it is clear what is being totaled and what it is divided by.

```dax
VAR numerator = SUM(FactSales[Revenue])
VAR denominator = SUM(FactSales[Quantity])
VAR result = DIVIDE(numerator, denominator)
RETURN result
```

## CALCULATE filter standards

Choose the filter behavior from the reporting question. These fragments use illustrative model fields and existing base measures; complete measures still follow the variable rules above. Company and date selections remain unless the example explicitly changes them.

### CALCULATE fixed revenue KPI — replace a selection

**Use when:** a dashboard's Revenue card should always show revenue, even when the Account Type slicer selects Expense. The measure defines its own account type.

```dax
VAR accountType = "Revenue"
VAR result = CALCULATE([Ledger Amount], Account[Account Type] = accountType)
RETURN result
```

This replaces the selection on Account Type only. Filters on individual accounts or account groups still apply, so this is not a way to ignore every Account filter.

### KEEPFILTERS expense breakdown — respect the selection

**Use when:** an account-type matrix has an Expense Amount column that should populate only expense rows. Revenue rows should be blank, rather than repeat the expense total.

```dax
VAR accountType = "Expense"
VAR result = CALCULATE([Ledger Amount], KEEPFILTERS(Account[Account Type] = accountType))
RETURN result
```

The row and the measure must both match. Expense rows return expenses; Revenue rows return blank for a SUM-based base measure. The grand total includes expenses only. A direct predicate would replace each row's Account Type and repeat expenses on Revenue rows.

### FILTER overspending departments — test a calculated result

**Use when:** a budget review needs actual expenses only from departments that are over budget for the selected period. Assume `[Expense Variance]` is actual minus budget, with overspending positive.

```dax
CALCULATE(
    [Actual Expense],
    FILTER(VALUES(Department[Department]), [Expense Variance] > 0)
)
```

`VALUES` limits the test to visible departments. `FILTER` evaluates the variance separately for each department and keeps the overspenders. A fixed field comparison cannot express this measure-based test. The result is their actual expenses, not the overspend amount.

### ALL department share — remove one selection

**Use when:** a department matrix needs each department's percentage of total expense. The denominator must include all departments, even when the Department slicer selects only one.

```dax
VAR totalExpense = CALCULATE([Actual Expense], ALL(Department[Department]))
VAR result = DIVIDE([Actual Expense], totalExpense)
RETURN result
```

Only the Department field's filter is removed. Company, date, and filters on other fields such as Department Group still apply. If the denominator should include only slicer-selected departments, this is not that calculation.

### ALLEXCEPT annual budget — retain only the year

**Use when:** a monthly budget report needs the full-year budget as a comparison beside each month. Fiscal Year is explicitly selected or appears on the visual.

```dax
CALCULATE([Budget Amount], ALLEXCEPT('Date', 'Date'[Fiscal Year]))
```

This keeps the Fiscal Year filter and removes month, quarter, date, and other Date-table filters. Use it only when ignoring all those other date selections is intentional. It does not infer a year from a selected month or date; without an explicit Fiscal Year filter, the result can include every year.

### USERELATIONSHIP invoice due dates — change the date basis

**Use when:** an invoice report normally groups amounts by invoice date, but finance also needs amounts by due date. The model has an inactive relationship from `FKDueDate` to Date.

```dax
CALCULATE([Invoice Amount], USERELATIONSHIP(Invoices[FKDueDate], 'Date'[PKDate]))
```

The selected month now applies to due dates rather than invoice dates. This changes which date relationship the measure uses, not the date selected in the report.

Empty matches return blank for a SUM-based measure. Zero requires the base measure or another expression to produce zero.

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
- [Microsoft `CALCULATE`](https://learn.microsoft.com/en-us/dax/calculate-function-dax)
- [Microsoft `USERELATIONSHIP`](https://learn.microsoft.com/en-us/dax/userelationship-function-dax)

# Semantic Model Measures

## Standards

### Measure naming standards

- Name base measures for their business value, such as `Sales Amount` or `Sales Quantity`.
- Name filtered measures `{Base Measure} | {Filter}` and reference the base measure instead of repeating its aggregation.
- Use `SUM` for additive base measures. Keep model-specific filtered measures in DAX, built from the base measure.

```dax
[Sales Amount] = SUM('Sales Transactions'[SalesAmount])
```

```dax
[Sales Amount | Intercompany] =
VAR result = CALCULATE([Sales Amount], KEEPFILTERS(Customer[Intercompany] = TRUE()))
RETURN result
```

### Measure visibility standards

- Expose business aggregations as explicit measures.
- Hide numeric columns not intended for direct aggregation or set `summarizeBy: none`.
- Give every visible measure a description; hidden helper measures can omit it.

### Measure format standards

- Give every visible measure an explicit format string.
- Align commas and decimal points within the visual.
- For aligned parenthesized negatives, use a dynamic format with non-breaking spaces and regular Segoe UI. Ordinary trailing spaces and bold/semibold fonts do not provide the required alignment.

```dax
"$ #,0" & UNICHAR(160) & ";$ (#,0);$ 0" & UNICHAR(160)
```

### Measure validation standards

- Establish the business definition, what is being counted or summed, report-filter behavior, and date-table requirements before writing the measure.
- Build and test incrementally.
- Check the base result, slicers, blank/zero/no-row cases, and a known control total when available.

## Default positions

### SQL or DAX defaults

Put organization-certified calculations in Gold SQL when multiple semantic models use them or are expected to. Otherwise, use DAX.

### Measure number-format defaults

Use these formats unless a project-specific format overrides them:

| Value | Format |
|---|---|
| Whole number | `#,###` |
| Percentage | `##%` |
| Currency | `$ #,0;-$ #,0;$ 0;--` |
