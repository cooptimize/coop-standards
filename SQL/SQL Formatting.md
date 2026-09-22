---
id: sql_formatting
title: SQL Formatting
domain: sql
layer: agnostic
artifact: agnostic
technology: agnostic
status: active
---
# SQL Formatting Rules

## Consistency when editing

- `JOIN` versus `INNER JOIN`, optional `AS`, and the operand order of an equality predicate are nonfunctional style differences. They are not defects in existing code.
- New statements and fully rewritten statements MUST use the canonical styles in this article.
- A targeted edit MUST preserve the statement's established style and MUST NOT reformat unrelated code solely to enforce a canonical style.
- Use one style consistently within each statement.

## SELECT

- In multiline lists, place each comma one character left of the first expression and use no space after it, so all expressions align.
- Use explicit projections; `SELECT *` MUST NOT be used.
- Every table and CTE reference MUST use an alias, even when only one source is referenced.
- Default aliases MUST be recognizable abbreviations of the source name, such as `salesline AS sl` and `salestable AS st`.
- When the same source is joined more than once or a short alias is ambiguous, append the source's role, such as `custtable AS ct_order` and `custtable AS ct_invoice`.
- Single-letter and ordinal aliases such as `t1` MUST NOT be used.
- In new and fully rewritten statements, use `AS` for table, CTE, and column aliases.
- Enclose every column alias in brackets, such as `AS [Customer Name]`. Do not bracket source identifiers by default.
- Do not use SQL reserved words as aliases. When an existing output contract requires one, enclose it in brackets.
- In `INSERT ... SELECT`, every expression MUST be aliased to its exact target column.

## CTEs

- Put `WITH` on its own line. Align CTE names; place each continuation comma one character left of the name with no following space.
- Name CTEs for their transformation, such as `ActiveCustomers`.
- Multi-step transformations MUST use CTEs instead of nested derived tables.
- Filter business rows in CTEs before joins.
- CTEs MUST preserve source field names unless a rename is required for the transformation. Apply target names in the final projection.

## Joins

- New and fully rewritten statements MUST use `INNER JOIN` or `LEFT JOIN`. They MUST NOT use bare `JOIN`, `RIGHT JOIN`, or `FULL OUTER JOIN`.
- Order multi-column join predicates from the broadest key to the most specific. For D365 F&O, place `dataareaid` first.
- In new and fully rewritten statements, place the table already in the `FROM`/join chain first and the table introduced by that `JOIN` second.
- `ON` clauses MUST contain only relationship predicates; `CASE` expressions and filter functions MUST NOT appear in them.

## EXISTS

- `EXISTS` and `NOT EXISTS` MAY be used.
- Each use MUST have a comment stating the tested condition and why it is used.

## Example

```sql
WITH
     ActiveCustomers AS
     (
         SELECT
               ct.accountnum
              ,ct.dataareaid
              ,ct.custgroup
         FROM bronze.raw_custtable AS ct
         WHERE ct.blocked = 0
     )
SELECT
      ac.accountnum AS [Customer]
     ,cg.name AS [CustomerGroup]
FROM ActiveCustomers AS ac
INNER JOIN bronze.raw_custgroup AS cg
    ON ac.dataareaid = cg.dataareaid
    AND ac.custgroup = cg.custgroup
WHERE EXISTS
(
    -- Tests for customer transactions without multiplying customer rows.
    SELECT 1
    FROM bronze.raw_custtrans AS ctr
    WHERE ctr.dataareaid = ac.dataareaid
        AND ctr.accountnum = ac.accountnum
);
```

```sql
INSERT INTO dim.Customer
(
      dataareaid
     ,customerid
     ,Customer
)
SELECT
      ct.dataareaid AS [dataareaid]
     ,ct.accountnum AS [customerid]
     ,ct.accountnum AS [Customer]
FROM bronze.raw_custtable AS ct;
```
