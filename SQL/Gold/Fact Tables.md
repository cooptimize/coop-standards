---
id: sql_gold_fact_tables
title: Gold Fact Tables
domain: sql
layer: gold
artifact: fact_table
technology: agnostic
status: active
---
# Gold Fact Tables

## Rules

- Use the `fact` schema and a PascalCase table name.
- Use PascalCase column names.
- Name dimension references `FK{DimensionName}`, such as `FKCustomer`.
- Name business-facing identifiers for the entity, such as `Customer`, not `CustomerId`.
- Make columns nullable by default.
- Do not add an identity column without a specific need.
- Where supported, add non-unique indexes to columns used for joins. An index does not enforce a relationship or uniqueness.

## Open decisions (non-normative)

- Names for multiple roles referencing one dimension and optional fact identities.
- Naming and types for currencies, quantities, percentages, dates, flags, codes, descriptions, and audit fields.
- Index naming, column order, index type, and physical FK constraints.

## Example

```sql
CREATE TABLE fact.CustomerTransactions
(
      FKCustomer bigint NULL
     ,Customer varchar(20) NULL
     ,Voucher varchar(20) NULL
     ,AmountMST decimal(19,4) NULL
);

-- Where supported
CREATE INDEX IX_CustomerTransactions_FKCustomer
    ON fact.CustomerTransactions (FKCustomer);
```
