<!-- ASSEMBLED from structured articles by scripts/assemble.py.
     Edit the source article under sql/, powerbi/, or tech/ and re-run
     `python3 scripts/assemble.py`. Do not hand-edit sections here. -->

# SQL Formatting Rules

## SELECT

- In multiline lists, place each comma one character left of the first expression and use no space after it, so all expressions align.
- Use explicit projections; `SELECT *` MUST NOT be used.
- Every table and CTE reference MUST use an alias, even when only one source is referenced.
- Default aliases MUST be recognizable abbreviations of the source name, such as `salesline AS sl` and `salestable AS st`.
- When the same source is joined more than once or a short alias is ambiguous, append the source's role, such as `custtable AS ct_order` and `custtable AS ct_invoice`.
- Single-letter and ordinal aliases such as `t1` MUST NOT be used.
- In `INSERT ... SELECT`, every expression MUST be aliased to its exact target column.

## CTEs

- Put `WITH` on its own line. Align CTE names; place each continuation comma one character left of the name with no following space.
- Name CTEs for their transformation, such as `ActiveCustomers`.
- Multi-step transformations MUST use CTEs instead of nested derived tables.
- Filter business rows in CTEs before joins.
- CTEs MUST preserve source field names unless a rename is required for the transformation. Apply target names in the final projection.

## Joins

- Only `INNER JOIN` and `LEFT JOIN` MAY be used. Bare `JOIN`, `RIGHT JOIN`, and `FULL OUTER JOIN` MUST NOT be used.
- Order multi-column join predicates from the broadest key to the most specific. For D365 F&O, place `dataareaid` first.
- In each join predicate, place the source-table expression first and the joined-table expression second.
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
      ac.accountnum AS Customer
     ,cg.name AS CustomerGroup
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
      ct.dataareaid AS dataareaid
     ,ct.accountnum AS customerid
     ,ct.accountnum AS Customer
FROM bronze.raw_custtable AS ct;
```

# Silver Deterministic Generation

## Generation boundary

- Silver objects MUST be produced by the approved deterministic process.
- Generated Silver SQL MUST NOT be authored or altered by an LLM.
- Changes to generated structure or behavior MUST be implemented in the source procedure or configuration.

## Documented behavior

The source procedures and configuration have not yet been provided. Add their approved transformation, naming, type, and indexing behavior here after direct review; do not infer it from generated output.

## Human-authored standards

Indexing rules MAY be human-authored. Route each approved article directly through `standards.yml` and implement its rules in the deterministic process.

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
      fs.PKCustomer AS FKCustomer
     ,fs.custaccount AS Customer
     ,fs.salesid AS SalesOrder
     ,fs.lineamount AS SalesAmount
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
SELECT fs.lineamount AS SalesAmount
FROM #FinalSales AS fs;

COMMIT TRANSACTION;
```

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

# Gold Views

## View naming

- Name views `{Schema}.{Entity}` with a PascalCase entity name.
- Use the `common` schema for views shared by multiple semantic models; otherwise use the semantic-model name, such as `sales.Customer`.

## Field organization

- Organize dimension views under `--Keys` and `--Attributes`.
- Organize fact views under `--Keys`, `--Attributes`, and `--Numbers`.
- Every fact view MUST include `NULL AS FKNULL` under `--Keys`.
- `--Numbers` MUST contain additive fact fields intended for `SUM`.
- Keys and numbers MUST retain their source names without aliases.
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
      cust.PKCustomer

    --Attributes
     ,cust.CustomerName AS [Customer Name]
     ,cust.Customer + ' • ' + cust.CustomerName AS [Customer and Name]
     ,cust.CustomerName + ' (' + cust.Customer + ')' AS [Name and (Customer)]
FROM dim.Customer AS cust;
```

### Fact

```sql
CREATE VIEW sales.Sales AS
SELECT
    --Keys
      NULL AS FKNULL
     ,sales.FKCustomer
     ,sales.FKDate

    --Attributes
     ,sales.SalesOrder AS [Sales Order]

    --Numbers
     ,sales.SalesAmount
     ,sales.Quantity
FROM fact.Sales AS sales;
```

# Fabric Warehouse Target Standards

Applies only to Fabric Warehouse. Persisted-column type restrictions apply when defining persisted columns, including tables created inside a stored procedure; they are not restrictions on view output or Azure SQL columns.

## Persisted column types

| MUST NOT use | Use instead |
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

These persisted-column restrictions MUST NOT be applied to Azure SQL targets. `coop-sql-review` MUST use its Azure SQL target mode when reviewing Azure SQL.

## Persisted expression types

CTAS projections MUST explicitly cast expressions whose resulting type must be controlled, including aggregate outputs used as persisted columns.

## Connections

- Fabric Warehouse `sqlcmd` calls MUST specify the database with `-d`.
- Fabric Warehouse connections MUST use Microsoft Entra authentication (`-G`); SQL authentication MUST NOT be used.
