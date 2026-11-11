<!-- ASSEMBLED from structured articles by scripts/assemble.py.
     Edit the source article under SQL/, Power BI/, or Technology/ and re-run
     `python3 scripts/assemble.py`. Do not hand-edit sections here. -->

# SQL Conventions

Standards are required. Default positions are starting choices for new code; follow an existing statement’s consistent style during targeted edits.

## Standards

### SELECT standards

- Use explicit projections. Never use `SELECT *`.
- In `INSERT ... SELECT`, alias every expression to its exact target column.
- List the target columns explicitly in every `INSERT ... SELECT`; do not rely on the table's physical column order.

```sql
INSERT INTO dim.Customer (Customer)
SELECT
      ct.accountnum AS Customer
FROM d365fo.custtable AS ct;
```

### DISTINCT standards

- Use `DISTINCT` only when the required result is one row per unique projected value.
- Never add `DISTINCT` to hide duplicate rows caused by an incorrect join, an incorrect grain, or a query whose duplication is not understood.

### Null-handling standards

- Use null-handling functions such as `ISNULL`, `COALESCE`, and `NULLIF` only in the `SELECT` projection. Do not use them in `FROM`, `JOIN`, `ON`, or `WHERE` logic.
- Use them for expected null behavior, such as presenting a missing value after a `LEFT JOIN`; do not use them to conceal incorrect source data or repair Silver data in a query.
- There is no repository-wide preference between `COALESCE` and `ISNULL`; use the function whose behavior fits the expression and target type.

### Function standards

- Do not wrap a column in a function unless the data proves the function is needed. This covers conversions (`CAST`, `CONVERT`, `TRY_CONVERT`, `TRY_CAST`), case and whitespace functions (`UPPER`, `LOWER`, `TRIM`, `LTRIM`, `RTRIM`), null handling, and every other scalar function.
- Proof comes from the source, not from habit: the column's declared type and length, its collation, or the actual values. When the columns being compared already share a type and collation, a conversion or case function changes nothing and must not be written.
- Never place a function on a column in a `JOIN`, `ON`, or `WHERE` predicate. A function there hides the column from indexes and statistics. If the two sides really differ, make them comparable at the source (fix the type or collation in Silver, or in the CTE that prepares the key), and record the mismatch as a defect.
- Every function that stays is documented by a `--` comment on the line above it that names the evidence: the source type, collation, or value pattern that requires it.
- A function in the projection that only restates the declared type, such as `CAST(x AS DATETIME2(6))` on a `DATETIME2(6)` column, is a defect.

```sql
-- Source stores the order date as NVARCHAR(10) in yyyy-MM-dd form; the target is DATE.
     ,TRY_CONVERT(DATE, sl.orderdate, 23) AS OrderDate
```

### Alias standards

- Alias every table and CTE reference, even when only one source is referenced.
- Do not use single-letter or ordinal aliases such as `t1`.
- Use square brackets only when required, such as names containing spaces or reserved words: `AS [Customer Name]`, but `AS Customer`. This applies to source identifiers and aliases, including views.
- When an existing output contract requires a SQL reserved word as an alias, enclose it in brackets.
- Qualify permanent table and view names with their schema. CTEs and temporary tables do not need schema qualification.
- Output aliases follow the target article: technical fields retain their required names; Gold view attributes use friendly names with spaces.

```sql
FROM d365fo.custtable AS ct
```

### CTE standards

- Use CTEs instead of nested derived tables for multi-step transformations.
- Preserve source field names through CTEs unless the transformation requires a rename. Apply target names in the final projection.

```sql
WITH
     ActiveCustomers AS (...)
```

### Join standards

- Never use `RIGHT JOIN`.
- Keep `ON` clauses limited to relationship predicates. Do not place `CASE` expressions or filter functions in them.

```sql
    LEFT JOIN dim.Customer AS cust
        ON sl.customerid = cust.customerid
```

### Comments standards

- Use only line comments in SQL: `-- ...`.
- Do not use block comments such as `/* ... */`.
- Use `--` comments to explain intent, assumptions, or the purpose of a conditional expression; keep them brief and directly tied to the code they describe.

```sql
-- Tests for customer sales without multiplying rows.
WHERE EXISTS (...)
```

### EXISTS standards

- `EXISTS` and `NOT EXISTS` are allowed.
- Add a comment stating the tested condition and why `EXISTS` is used.

```sql
-- Tests for customer sales without multiplying rows.
WHERE EXISTS (...)
```

### Error-handling standards

- Keep SQL lean. Do not add `TRY`/`CATCH`, `THROW`, `RAISERROR`, `@@ERROR` or `@@ROWCOUNT` checks, `IF EXISTS` guards, or other defensive checks unless the project's standards ask for them. Let an error stop the statement and reach the caller or the orchestrating pipeline.
- Put validation outside the object, in separate test queries: row counts, grain, duplicate keys, orphaned foreign keys, and expected totals. Hand them over with the change and run them on dev after it is deployed.
- When editing existing code that already has error handling, leave it as it is unless the change is about it.

## Default positions

### Defaults when editing existing code

- `JOIN` versus `INNER JOIN`, optional `AS`, and equality-operand order are nonfunctional differences. They are not defects in existing code.
- Preserve the statement's established style during a targeted edit. Do not change unrelated code solely to enforce a default.
- Use one style consistently within each statement.

### Alias defaults

- Use recognizable source abbreviations, such as `salesline AS sl` and `salestable AS st`.
- Use lowercase source aliases. When a source is joined more than once or an abbreviation is ambiguous, use `{abbreviation}_{role}`, such as `ct_order` and `ct_invoice`.
- Use `AS` for table, CTE, and column aliases.
- Avoid SQL reserved words as aliases.

```sql
custtable AS ct_order
custtable AS ct_invoice
```

### CTE and temporary-table defaults

- Use CTEs when they produce the required result without a demonstrated performance problem.
- Use a temporary table when the intermediate result is reused or when it resolves a demonstrated performance problem.
- Name CTEs in PascalCase for their transformation, such as `ActiveCustomers`.
- Filter business rows in CTEs before joins.

```sql
ActiveCustomers AS (...)
```

### Set operator defaults

- Use `UNION ALL`.
- Use `UNION` only when removing duplicate rows across the combined result sets is an intentional requirement.

### Table-hint defaults

Do not use `NOLOCK` by default. Cooptimize normally queries replicated or warehouse data rather than an active production ERP database. Use `NOLOCK` only for an explicitly approved case where dirty-read behavior is acceptable.

### Join defaults

- Use explicit `INNER JOIN` or `LEFT JOIN` for new and fully rewritten statements.
- Use `LEFT JOIN`, not `LEFT OUTER JOIN`; omit the optional `OUTER` keyword.
- Do not use `FULL OUTER JOIN` by default.
- Within each `ON` clause, order join conditions from the most general key to the most specific: for example, company (`dataareaid`) before sales order (`salesid`).
- Place the table already in the `FROM`/join chain first and the table introduced by that `JOIN` second.

```sql
    INNER JOIN d365fo.salestable AS st
        ON sl.dataareaid = st.dataareaid
        AND sl.salesid   = st.salesid
```

### Join order defaults

- Start `FROM` with the most detailed source table, such as sales lines rather than sales headers.
- List `INNER JOIN` clauses first, followed by `LEFT JOIN` clauses.
- Favor larger tables earlier and smaller lookup tables later.
- Respect dependencies: a join that uses an earlier table's fields must follow that table. These are ordering guidelines; do not reorder joins when doing so changes which rows are returned.

```sql
FROM d365fo.salesline            AS sl
    INNER JOIN d365fo.salestable AS st
        ON ...
    LEFT JOIN dim.Customer       AS cust
        ON ...
```

### Missing-match defaults

Use `NOT EXISTS` for missing-match checks when the comparison can contain NULL. `NOT IN (subquery)` can return no matches when the subquery includes NULL; it is not interchangeable with `NOT EXISTS`. Decide separately how a NULL outer key should behave.

```sql
-- Finds customers with no matching sales orders.
WHERE NOT EXISTS (...)
```

## Supporting references

- [Microsoft: NULL behavior with IN and NOT IN](https://learn.microsoft.com/en-us/sql/t-sql/language-elements/in-transact-sql)

# SQL Layout

These rules define how SQL is displayed. Apply them to new or fully reformatted statements. During a targeted edit, leave unrelated formatting alone.

## Standards

### SELECT layout standards

- In multiline lists, place each comma one character left of the first expression with no following space.
- Within each contiguous projection section, align column-alias `AS` keywords at the same visual column. A blank line or organizing comment starts a new section.
- CTE definitions and `CREATE ... AS` do not use column-alias alignment. Table-source aliases follow the join layout standards below.

```sql
SELECT
      ct.accountnum AS Customer
     ,ct.name       AS [Customer Name]
```

### CTE layout standards

- Put `WITH` on its own line.
- Align CTE names. Place each continuation comma one character left of the CTE name with no following space.

```sql
WITH
     ActiveCustomers AS (...)
    ,SalesOrders AS (...)
```

### Join layout standards

- Indent joins four spaces beneath `FROM`. Indent `ON` and its additional `AND` predicates four spaces beneath the join, at the same indentation.
- Align table-source `AS` keywords across the `FROM` and joins in the same query block. Do not align across separate queries or CTE definitions.
- Align `=` signs within each join's `ON` clause; start alignment afresh for the next join.
- Use SQL Prompt's alias alignment and comparison-operator alignment options.

```sql
FROM OrderAmounts                AS oa
    INNER JOIN d365fo.salestable AS st
        ON oa.dataareaid = st.dataareaid
        AND oa.salesid   = st.salesid
    LEFT JOIN d365fo.custtable   AS ct
        ON st.dataareaid   = ct.dataareaid
        AND st.custaccount = ct.accountnum
```

### SQL Prompt bracket setting

Use **Remove unnecessary square brackets** when formatting with SQL Prompt. Keep required brackets, such as `AS [Customer Name]`; remove optional ones, such as `AS [Customer]`.

## Default positions

### Indentation defaults

Use spaces so alignment survives different editor tab settings. At the outermost level, examples use six spaces before SELECT expressions and five before CTE names; each list's comma sits one column earlier. The lists align internally, not with each other.

### Clause layout defaults

Start `SELECT`, `FROM`, `WHERE`, `GROUP BY`, and `ORDER BY` on separate lines aligned with each other. Use the SELECT list layout for multiline grouping and ordering lists. Put additional WHERE conditions on separate indented lines; preserve parentheses that control mixed AND/OR logic.

```sql
FROM d365fo.custtable AS ct
WHERE ct.blocked = 0
    AND ct.dataareaid = 'usmf'
```

### CASE layout defaults

Put each `WHEN` and `ELSE` on a separate indented line. Align `END` with `CASE` and keep the output alias after `END`.

```sql
CASE
    WHEN ct.blocked = 0 THEN 'Available'
    ELSE 'Blocked'
END AS [Customer Status]
```

### EXISTS comment defaults

Put the explanation immediately above the `WHERE` or `AND` containing `EXISTS` or `NOT EXISTS`. Plain prose is enough; no fixed comment template is required.

## Stored procedure layout example

This reporting procedure summarizes nonzero sales lines by company and sales order, labels missing customer records, and includes only customers with posted transactions. It demonstrates layout, not a Gold loading pattern. Assume the D365FO tables are available under `d365fo`.

```sql
CREATE OR ALTER PROCEDURE reporting.SalesOrderSummary
AS
BEGIN
    SET NOCOUNT ON;

    WITH
         IncludedLines AS
         (
             SELECT
                   sl.dataareaid
                  ,sl.salesid
                  ,sl.lineamount
             FROM d365fo.salesline AS sl
             WHERE sl.salesid <> ''
                 AND sl.lineamount <> 0
         )
        ,OrderAmounts AS
         (
             SELECT
                   il.dataareaid
                  ,il.salesid
                  ,SUM(il.lineamount) AS lineamount
             FROM IncludedLines AS il
             GROUP BY
                   il.dataareaid
                  ,il.salesid
         )
    SELECT
        -- Order attributes
          oa.dataareaid  AS Company
         ,oa.salesid     AS [Sales Order]
         ,st.custaccount AS Customer
         ,CASE
              WHEN ct.accountnum IS NULL THEN 'Missing customer'
              ELSE 'Matched customer'
          END            AS [Customer Match]

        -- Amounts
         ,oa.lineamount AS [Sales Amount]
    FROM OrderAmounts                AS oa
        INNER JOIN d365fo.salestable AS st
            ON oa.dataareaid = st.dataareaid
            AND oa.salesid   = st.salesid
        LEFT JOIN d365fo.custtable   AS ct
            ON st.dataareaid   = ct.dataareaid
            AND st.custaccount = ct.accountnum
    -- Require posted customer activity without multiplying sales-order rows.
    WHERE EXISTS
    (
        SELECT 1
        FROM d365fo.custtrans AS ctr
        WHERE st.dataareaid = ctr.dataareaid
            AND st.custaccount = ctr.accountnum
    )
    ORDER BY
          oa.dataareaid
         ,oa.salesid;
END;
```

## Supporting references

- [Redgate SQL Prompt: Add/remove square brackets](https://documentation.red-gate.com/sp10/sql-refactoring/sql-prompt-actions)
- [Redgate SQL Prompt: table-alias alignment in joins](https://documentation.red-gate.com/sp9/release-notes-and-other-versions/sql-prompt-8-0-release-notes)
- [Thinkwise: SQL Prompt style and comparison alignment](https://docs.thinkwisesoftware.com/docs/sf/guidelines_sql_formatting#comparison-alignment)

# Silver Tables

Silver tables reproduce source-system tables for downstream use. Keep their structure and data types close to the source; put reporting logic and dimensional modeling in Gold.

## Standards

### Source structure standards

- Keep each Silver table structurally aligned with its source table.
- Match source data types, string lengths, numeric precision and scale, and date/time precision when the target platform supports them.
- When the target does not support a source type, use the closest compatible type allowed by that platform.
- Do not change Silver types for reporting, presentation, or semantic-model convenience.

### Schema Manager standards

Schema Manager creates and maintains Silver tables for supported Dynamics 365 and Dataverse sources, including Finance and Operations, Project Operations, Customer Engagement, and custom Dataverse applications.

- Use Schema Manager to create or change these table definitions.
- Do not manually create or alter Schema Manager-managed definitions except for the two approved changes below.
- Do not use an LLM to create or alter Schema Manager-generated SQL.
- Change generated behavior through Schema Manager procedures, configuration, or metadata.

### Approved developer changes

Developers may make these two changes to a Schema Manager-managed table:

1. Increase a `VARCHAR` length when source data does not fit the generated length. Change only the affected column and use the smallest length that safely holds the source data.
2. Create, change, or remove custom indexes when the workload requires them.

Schema Manager must preserve increased `VARCHAR` lengths and custom indexes when it updates or rebuilds the table. A later run must not shrink an approved length or require a developer to recreate an index.

### Other source-system standards

Schema Manager rules do not apply to a source system it does not support. For those sources:

- Keep the Silver table as close to the source representation as the target permits.
- Use the closest compatible target type when the source type is unavailable.
- Put business transformations and dimensional modeling downstream unless ingestion itself requires a change.

## Default positions

### Recurring schema mismatch defaults

When the same schema mismatch recurs, correct the Schema Manager metadata, configuration, or type-mapping logic instead of repeatedly changing individual tables.

# Gold Stored Procedures

Convert raw data into the final Gold fact or dimension shape. Organize applicable work as Removal, Gather, Transform, and Write. Loading recipes belong in the separate patterns knowledge base.

## Removal standards

Remove existing data only when the selected loading pattern requires it. The pattern and target technology determine whether to use `TRUNCATE`, `DELETE`, or another method.

```sql
TRUNCATE TABLE fact.Sales;
```

## Gather standards

Gather source data with CTEs or temporary tables. Preserve intermediate field names according to SQL Conventions.

```sql
FROM d365fo.salesline            AS sl
    INNER JOIN d365fo.salestable AS st
        ON sl.dataareaid = st.dataareaid
        AND sl.salesid   = st.salesid
```

## Transformation standards

Resolve keys, joins, filters, and business transformations in the stored procedure. Apply target field names in the final write projection.

```sql
    INNER JOIN dim.Customer AS cust
        ON sl.dataareaid   = cust.dataareaid
        AND sl.custaccount = cust.customerid
```

## Write standards

Write the completed rows without adding business logic. The loading pattern and target technology determine whether to use `INSERT`, `MERGE`, or another method.

```sql
INSERT INTO fact.Sales (FKCustomer,SalesAmount)
SELECT
      fs.PKCustomer AS FKCustomer
     ,fs.lineamount AS SalesAmount
FROM #FinalSales AS fs;
```

## Comment standards

Explain why a non-obvious choice exists; do not narrate the SQL. Phase comments are allowed to separate long procedures.

```sql
-- A full refresh requires the prior snapshot to be removed.
```

## Error-handling standards

Keep the procedure to the four phases. Do not add `TRY`/`CATCH`, `THROW`, `RAISERROR`, row-count assertions or other defensive checks unless the project's standards ask for them; validation runs as separate test queries after the load, as SQL Conventions describe.

## Preventing empty or partial tables

- Use an explicit transaction when DirectQuery, integrations, or other live consumers require removal and replacement to commit together.
- A failed statement must roll back the whole transaction without error-handling code. In Fabric Warehouse a failed statement rolls back the transaction on its own. In SQL Server and Azure SQL, put `SET XACT_ABORT ON;` before `BEGIN TRANSACTION` so any error rolls back the transaction and stops the procedure. Do not wrap the transaction in `TRY`/`CATCH`.
- Limit the transaction to statements that need to become visible together. Gather and transform beforehand when the loading pattern permits; long transactions increase blocking, conflicts, and resource use.
- Use this only when required by the incremental or replacement strategy.
- A standalone `MERGE` commits its changes together under autocommit. Use an explicit transaction when it needs to commit with other statements.

```sql
-- Any error rolls back the removal and the write together (SQL Server, Azure SQL).
SET XACT_ABORT ON;

BEGIN TRANSACTION;
-- Removal and writing occur here.
COMMIT TRANSACTION;
```

# Gold Fact Tables

## Standards

### Fact naming standards

- Use `fact` and PascalCase table and column names.
- Name dimension references `FK{DimensionName}`.
- Name business-facing identifiers for the entity: `Customer`, not `CustomerId`.

```sql
CREATE TABLE fact.CustomerTransactions (...)
      FKCustomer bigint NULL
```

### Fact index standards

Where supported, add non-unique indexes to join columns. Indexes do not enforce relationships or uniqueness.

```sql
CREATE INDEX IX_CustomerTransactions_FKCustomer
    ON fact.CustomerTransactions (FKCustomer);
```

## Default positions

### Fact column defaults

- Make columns nullable.
- Add an identity column only when there is a specific need.

```sql
     ,Customer varchar(20) NULL
     ,AmountMST decimal(19,4) NULL
```

# Gold Dimension Tables

## Standards

### Dimension naming standards

- Use `dim` and a PascalCase table name.
- Name the identity `PK{DimensionName}` and use the target's standard identity behavior.
- Keep lowercase source names for business matching fields, such as `dataareaid` and `customerid`. These fields can be nullable, combined, and non-unique.
- Name business-facing identifiers for the entity: `Customer`, not `CustomerId`. Use PascalCase for other columns.

```sql
CREATE TABLE dim.Customer (...)
      PKCustomer bigint IDENTITY NOT NULL
```

### Dimension matching standards

- Where supported, index fields used together for matching with a composite, non-unique index.
- Do not create an artificial missing-match row, such as key `-1` named `Unknown`.

```sql
CREATE INDEX IX_Customer_dataareaid_customerid
    ON dim.Customer (dataareaid,customerid);
```

## Default positions

### Dimension nullability defaults

Make every column except the identity nullable. Population is controlled by the stored procedure.

```sql
     ,customerid varchar(20) NULL
     ,CustomerName varchar(100) NULL
```

## Open decisions (not standards)

- Naming and types for numbers, dates, flags, codes, descriptions, and audit fields.
- Index names, column order, index type, and physical constraints on the identity key.

# Gold Views

## View naming standards

Use `{Schema}.{Entity}` with a PascalCase entity name. Use `common` for views shared by semantic models; otherwise use the model name.

```sql
CREATE VIEW sales.Customer AS
```

## View field standards

- Give every projected field an explicit alias, including unchanged names. Use brackets only when the name requires them.
- Organize dimensions under `--Keys` and `--Attributes`; add `--Numbers` for facts.
- Include `NULL AS FKNULL` in every fact view's keys.
- Keep key and number names unchanged. Numbers are additive fact fields intended for `SUM`.
- Give attributes friendly names with spaces.
- Exclude helper join fields such as `dataareaid` and `customerid`.

### Dimension view example

```sql
SELECT
    --Keys
      cust.PKCustomer   AS PKCustomer
    --Attributes
     ,cust.CustomerName AS [Customer Name]
FROM dim.Customer AS cust;
```

### Fact view example

```sql
SELECT
    --Keys
      NULL             AS FKNULL
     ,sales.FKCustomer AS FKCustomer
    --Attributes
     ,sales.SalesOrder AS [Sales Order]
    --Numbers
     ,sales.SalesAmount AS SalesAmount
FROM fact.Sales AS sales;
```

## Dimension display-field standards

When a dimension has an identifier and name, include both combined fields: identifier first for pivot reporting, and name first with the identifier in parentheses for alphabetical reporting.

```sql
     ,cust.Customer + ' • ' + cust.CustomerName      AS [Customer and Name]
     ,cust.CustomerName + ' (' + cust.Customer + ')' AS [Name and (Customer)]
```

## View transformation standards

The two dimension display fields above are approved transformations. Other transformations and all joins require an explicit user request, a necessity check, and a comment explaining the exception. Otherwise, put transformations in stored procedures.

# Fabric Warehouse

Applies only to Fabric Warehouse. Persisted-column type restrictions apply when defining persisted columns, including tables created inside a stored procedure; they are not restrictions on view output or Azure SQL columns.

## Fabric persisted-column standards

| Do not use | Use instead |
|---|---|
| `nvarchar`, `nchar` | `varchar`, `char` |
| `datetime`, `smalldatetime` | `datetime2` |
| `datetimeoffset` | `datetime2`; apply offset/time-zone logic at query time |
| `money`, `smallmoney` | `decimal(19,4)` |
| `tinyint` | `smallint` |
| `text`, `ntext` | `varchar(max)` |
| `image` | `varbinary(max)` |
| `xml` | `varchar(max)` |
| `json` | `varchar(max)` |
| `geography`, `geometry` | latitude/longitude columns, WKB `varbinary`, or WKT `varchar` |
| `hierarchyid`, CLR user-defined types | a supported native type |

Do not apply these persisted-column restrictions to Azure SQL. Select Azure SQL target mode when reviewing Azure SQL with `coop-sql-review`.

## Fabric persisted-expression standards

In CTAS projections, explicitly cast expressions when the persisted type needs to be controlled, including aggregate outputs.

```sql
     ,CAST(SUM(sl.lineamount) AS decimal(19,4)) AS SalesAmount
```

## Fabric connection standards

- Specify the database with `-d` in Fabric Warehouse `sqlcmd` calls.
- Use Microsoft Entra authentication (`-G`), never SQL authentication.

```text
sqlcmd -S <warehouse-endpoint> -d <database> -G
```
