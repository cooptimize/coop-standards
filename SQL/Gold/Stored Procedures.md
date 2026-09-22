---
id: sql_gold_stored_procedures
title: Gold Stored Procedures
domain: sql
layer: gold
artifact: stored_procedure
technology: agnostic
status: active
---
# Gold Stored Procedures

## Responsibility

- Convert source-shaped data into the final Gold fact or dimension shape and write it to the target.
- Keep joins, filters, derivations, and business transformations in stored procedures rather than views.
- Organize applicable work as Removal, Gather, Transform, and Write.
- Phase comments MAY separate long procedures. Explanatory comments MUST state why a non-obvious choice exists, not narrate the SQL.

## Removal

- Remove target data only when required by the selected loading pattern.
- Loading-pattern and technology guidance determine whether to use `TRUNCATE`, `DELETE`, or another removal method.

```sql
-- A full refresh requires the prior snapshot to be removed.
TRUNCATE TABLE fact.Sales;
```

## Gather

- Gather required source data with CTEs or temporary tables.
- Formatting rules govern CTE layout and intermediate field names.

```sql
SELECT
      sl.dataareaid
     ,st.custaccount
     ,sl.salesid
     ,sl.lineamount
INTO #SalesLines
FROM d365fo.salesline AS sl
INNER JOIN d365fo.salestable AS st
    ON sl.dataareaid = st.dataareaid
    AND sl.salesid = st.salesid;
```

## Transform

- Resolve keys, joins, derivations, and other business logic into the final row shape.
- Apply target field names only in the final write projection.

```sql
SELECT
      cust.PKCustomer
     ,sl.custaccount
     ,sl.salesid
     ,sl.lineamount
INTO #FinalSales
FROM #SalesLines AS sl
INNER JOIN dim.Customer AS cust
    ON sl.dataareaid = cust.dataareaid
    AND sl.custaccount = cust.customerid;
```

## Write

- Write the completed rowset without adding business logic.
- Loading-pattern and technology guidance determine whether to use `INSERT`, `MERGE`, or another method.

```sql
INSERT INTO fact.Sales
(
      FKCustomer
     ,Customer
     ,SalesOrder
     ,SalesAmount
)
SELECT
      fs.PKCustomer  AS [FKCustomer]
     ,fs.custaccount AS [Customer]
     ,fs.salesid     AS [SalesOrder]
     ,fs.lineamount  AS [SalesAmount]
FROM #FinalSales AS fs;
```

## Preventing empty or partial tables

- Wrap removal and writing in one explicit transaction when DirectQuery, integrations, or other live consumers MUST see either the previous table contents or the completed replacement.
- Use `BEGIN TRANSACTION`, then `COMMIT TRANSACTION` on success or `ROLLBACK TRANSACTION` on failure.
- Keep the transaction limited to statements that must become visible together. Gather and transform before opening it when the loading pattern permits; long transactions can increase blocking, conflicts, and resource use.
- Use this behavior only when required by the selected incremental or replacement strategy.
- A standalone `MERGE` commits all of its changes together under autocommit. Use an explicit transaction when it must commit together with other statements.

```sql
BEGIN TRANSACTION;

TRUNCATE TABLE fact.Sales;

INSERT INTO fact.Sales (SalesAmount)
SELECT fs.lineamount AS [SalesAmount]
FROM #FinalSales AS fs;

COMMIT TRANSACTION;
```
