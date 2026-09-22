---
id: sql_gold_dimension_tables
title: Gold Dimension Tables
domain: sql
layer: gold
artifact: dimension_table
technology: agnostic
status: active
---
# Gold Dimension Tables

## Rules

- Use the `dim` schema and a PascalCase table name.
- Name the identity column `PK{DimensionName}`, such as `PKCustomer`, and use the target's standard identity behavior.
- Preserve lowercase D365 F&O source names for nullable matching fields, such as `dataareaid` and `customerid`. Matching may use multiple fields and does not imply uniqueness.
- Name business-facing identifiers for the entity without using "Id" or "id", such as `Customer`, not `CustomerId`.
- Use PascalCase for all other columns.
- Make all columns except the identity nullable by default.
- Where supported, add a composite, non-unique index to fields used together for matching. The index does not enforce uniqueness.
- Do not create a placeholder row for missing matches, such as key `-1` named `Unknown`.

## Open decisions (non-normative)

- Naming and types for numeric, date/time, flag, code, description, and audit fields.
- Index naming, column order, index type, and physical identity-key constraints.

## Example

```sql
CREATE TABLE dim.Customer
(
      PKCustomer bigint IDENTITY NOT NULL
     ,dataareaid varchar(4) NULL
     ,customerid varchar(20) NULL
     ,Customer varchar(20) NULL -- account number
     ,CustomerName varchar(100) NULL
);

-- Where supported
CREATE INDEX IX_Customer_dataareaid_customerid
    ON dim.Customer
    (
          dataareaid
         ,customerid
    );
```
