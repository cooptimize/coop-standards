---
id: sql_gold_views
title: Gold Views
domain: sql
layer: gold
artifact: view
technology: agnostic
status: active
---
# Gold Views

## View naming

- Name views `{Schema}.{Entity}` with a PascalCase entity name.
- Use the `common` schema for views shared by multiple semantic models; otherwise use the semantic-model name, such as `sales.Customer`.

## Field organization

- Every projected field MUST use a bracketed alias, including fields whose output name is unchanged.
- Organize dimension views under `--Keys` and `--Attributes`.
- Organize fact views under `--Keys`, `--Attributes`, and `--Numbers`.
- Every fact view MUST include `NULL AS [FKNULL]` under `--Keys`.
- `--Numbers` MUST contain additive fact fields intended for `SUM`.
- Keys and numbers MUST retain their source names through same-name aliases.
- Attributes MUST use friendly aliases with spaces, such as `CustomerName AS [Customer Name]`.

## Additional dimension fields

- A dimension view with an entity identifier and name MUST include both presentation fields:
  - `{Entity} + ' • ' + {Entity}Name AS [{Entity} and Name]` for identifier-first reporting.
  - `{Entity}Name + ' (' + {Entity} + ')' AS [Name and ({Entity})]` for alphabetical reporting.

## Hidden fields

- Helper join fields, including `dataareaid` and `customerid`, MUST NOT be exposed.

## Transformations and joins

- The two dimension presentation fields above are approved view transformations. Other transformations and all joins MUST NOT be used unless the user explicitly requests them and they are necessary. Transformations otherwise belong in stored procedures.
- An approved exception MUST include a comment explaining why the join or transformation is necessary in the view.

## Example

### Dimension

```sql
CREATE VIEW sales.Customer AS
SELECT
    --Keys
      cust.PKCustomer AS [PKCustomer]

    --Attributes
     ,cust.CustomerName                              AS [Customer Name]
     ,cust.Customer + ' • ' + cust.CustomerName      AS [Customer and Name]
     ,cust.CustomerName + ' (' + cust.Customer + ')' AS [Name and (Customer)]
FROM dim.Customer AS cust;
```

### Fact

```sql
CREATE VIEW sales.Sales AS
SELECT
    --Keys
      NULL             AS [FKNULL]
     ,sales.FKCustomer AS [FKCustomer]
     ,sales.FKDate     AS [FKDate]

    --Attributes
     ,sales.SalesOrder AS [Sales Order]

    --Numbers
     ,sales.SalesAmount AS [SalesAmount]
     ,sales.Quantity    AS [Quantity]
FROM fact.Sales AS sales;
```
