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

### EXISTS standards

- `EXISTS` and `NOT EXISTS` are allowed.
- Add a comment stating the tested condition and why `EXISTS` is used.

```sql
-- Tests for customer sales without multiplying rows.
WHERE EXISTS (...)
```

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

### CTE defaults

- Name CTEs in PascalCase for their transformation, such as `ActiveCustomers`.
- Filter business rows in CTEs before joins.

```sql
ActiveCustomers AS (...)
```

### Join defaults

- Use explicit `INNER JOIN` or `LEFT JOIN` for new and fully rewritten statements.
- Use `LEFT JOIN`, not `LEFT OUTER JOIN`; omit the optional `OUTER` keyword.
- Do not use `FULL OUTER JOIN` by default.
- Within each `ON` clause, order join conditions from the most general key to the most specific: for example, company (`dataareaid`) before sales order (`salesid`).
- Place the table already in the `FROM`/join chain first and the table introduced by that `JOIN` second.

```sql
INNER JOIN d365fo.salestable AS st
    ON sl.dataareaid = st.dataareaid
        AND sl.salesid = st.salesid
```

### Join order defaults

- Start `FROM` with the most detailed source table, such as sales lines rather than sales headers.
- List `INNER JOIN` clauses first, followed by `LEFT JOIN` clauses.
- Favor larger tables earlier and smaller lookup tables later.
- Respect dependencies: a join that uses an earlier table's fields must follow that table. These are ordering guidelines; do not reorder joins when doing so changes which rows are returned.

```sql
FROM d365fo.salesline AS sl
INNER JOIN d365fo.salestable AS st
    ON ...
LEFT JOIN dim.Customer AS cust
    ON ...
```

### Missing-match defaults

Use `NOT EXISTS` for missing-match checks when the comparison can contain NULL. `NOT IN (subquery)` can return no matches when the subquery includes NULL; it is not interchangeable with `NOT EXISTS`. Decide separately how a NULL outer key should behave.

```sql
-- Finds customers with no matching sales orders.
WHERE NOT EXISTS (...)
```

## Open decisions (non-normative)

- Defaults for `UNION` versus `UNION ALL`, use of `DISTINCT`, `COALESCE` versus `ISNULL`, and table hints such as `NOLOCK` are not defined.
- Stored procedures allow CTEs and temporary tables; criteria for choosing between them are not defined.

## References (non-normative)

- [Microsoft: NULL behavior with IN and NOT IN](https://learn.microsoft.com/en-us/sql/t-sql/language-elements/in-transact-sql)

# SQL Layout

These rules define how SQL is displayed. Apply them to new or fully reformatted statements. During a targeted edit, leave unrelated formatting alone.

## Standards

### SELECT layout standards

- In multiline lists, place each comma one character left of the first expression with no following space.
- Within each contiguous projection section, align column-alias `AS` keywords at the same visual column. A blank line or organizing comment starts a new section.
- Do not align `AS` used for tables, CTEs, or `CREATE ... AS`.

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

Indent `ON` four spaces beneath the join and each additional predicate four spaces beneath `ON`.

```sql
INNER JOIN d365fo.salestable AS st
    ON ct.dataareaid = st.dataareaid
        AND ct.accountnum = st.custaccount
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

## References (non-normative)

- [Redgate SQL Prompt: Add/remove square brackets](https://documentation.red-gate.com/sp10/sql-refactoring/sql-prompt-actions)

# Silver Layer

Silver preserves source-system structure and data types as closely as
the target platform allows. Dynamics 365 and Dataverse sources use
Schema Manager for deterministic Silver generation.

## Standards

### Silver schema standards

-   Keep Silver tables structurally aligned with their source tables.
-   Match source column data types as closely as the target platform
    supports.
-   Preserve source string lengths, numeric precision and scale, and
    date/time precision where supported.
-   When the target platform does not support the source type, use the
    closest compatible target type.
-   Do not change a Silver data type solely for downstream reporting,
    presentation, or semantic-model convenience.
-   Apply target-technology type restrictions where required by the
    platform.

### Dynamics 365 and Dataverse standards

These standards apply to data sourced from:

-   Dynamics 365 Finance & Operations (F&O).
-   Dynamics 365 Project Operations.
-   Dynamics 365 Customer Engagement (CE).
-   Custom Dataverse applications and tables.

They apply when these sources are replicated into Azure Data Lake or
Microsoft OneLake for Azure- and Fabric-based implementations,
respectively.

-   Manage these Silver tables through the approved Schema Manager
    process.
-   Treat the generated table definition and lifecycle as owned by
    Schema Manager.
-   Do not manually alter Schema Manager-managed structures except for
    documented exceptions.
-   Do not use an LLM to author or alter generated Silver SQL.
-   Change generated behavior through Schema Manager procedures,
    configuration, metadata, or other supported mechanisms.

See [Schema Manager](Schema%20Manager.md) for generation and lifecycle
standards.

### Other source systems

Schema Manager requirements do not apply to source systems that have not
been incorporated into Schema Manager.

-   Match Silver columns to the source table data types as closely as
    the target platform supports.
-   Keep the Silver table as close to the source representation as
    practical.
-   Use the closest compatible target type when the source type is not
    supported.
-   Perform business-oriented transformations and dimensional modeling
    downstream unless the Silver ingestion process requires otherwise.

## Documented exceptions

-   See [Schema Derivation](Schema%20Derivation.md) for source metadata
    and `VARCHAR` length exceptions.
-   See [Indexing](Indexing.md) for developer-managed Silver indexes.

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
FROM d365fo.salesline AS sl
INNER JOIN d365fo.salestable AS st
    ON sl.dataareaid = st.dataareaid
        AND sl.salesid = st.salesid
```

## Transformation standards

Resolve keys, joins, filters, and business transformations in the stored procedure. Apply target field names in the final write projection.

```sql
INNER JOIN dim.Customer AS cust
    ON sl.dataareaid = cust.dataareaid
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

## Preventing empty or partial tables

- Use an explicit transaction when DirectQuery, integrations, or other live consumers require removal and replacement to commit together.
- Commit on success; roll back on failure.
- Limit the transaction to statements that need to become visible together. Gather and transform beforehand when the loading pattern permits; long transactions increase blocking, conflicts, and resource use.
- Use this only when required by the incremental or replacement strategy.
- A standalone `MERGE` commits its changes together under autocommit. Use an explicit transaction when it needs to commit with other statements.

```sql
BEGIN TRANSACTION;
-- Removal and writing occur here; roll back on failure.
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

## Open decisions (non-normative)

- Names for multiple references to one dimension and optional fact identities.
- Naming and types for currencies, quantities, percentages, dates, flags, codes, descriptions, and audit fields.
- Index names, column order, index type, and physical foreign-key constraints.

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

## Open decisions (non-normative)

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
