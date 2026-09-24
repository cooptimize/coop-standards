---
id: sql_formatting
title: SQL Layout
domain: sql
layer: agnostic
artifact: formatting
technology: agnostic
status: active
---
# SQL Layout

These rules define how SQL is displayed. Apply them to new or fully reformatted statements. During a targeted edit, leave unrelated formatting alone.

## SELECT layout standards

- In multiline lists, place each comma one character left of the first expression with no following space.
- Within each contiguous projection section, align column-alias `AS` keywords at the same visual column. A blank line or organizing comment starts a new section.
- Do not align `AS` used for tables, CTEs, or `CREATE ... AS`.

```sql
SELECT
      ct.accountnum AS [Customer]
     ,ct.name       AS [Customer Name]
```

## CTE layout standards

- Put `WITH` on its own line.
- Align CTE names. Place each continuation comma one character left of the CTE name with no following space.

```sql
WITH
     ActiveCustomers AS (...)
    ,SalesOrders AS (...)
```

## Join layout standards

Indent `ON` four spaces beneath the join and each additional predicate four spaces beneath `ON`.

```sql
INNER JOIN d365fo.salestable AS st
    ON ct.dataareaid = st.dataareaid
        AND ct.accountnum = st.custaccount
```
