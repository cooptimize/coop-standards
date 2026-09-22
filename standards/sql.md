# SQL Standards

Canonical Cooptimize SQL policy. Existing numbered sections are preserved so current `coop-sql-review` `standard_ref` citations remain valid.

## 1. Naming Conventions

- Tables MUST use `layer.object_name` naming, for example `bronze.raw_d365_contact` or `silver.dim_customer`.
- CTE names MUST use the `cte_` prefix and a descriptive name, for example `cte_cleaned_contacts`.
- Bronze columns MUST preserve source-system column names.
- Silver and Gold columns MUST use PascalCase.

## 2. Descriptive Aliases

- Table aliases MUST describe the entity and MUST NOT be single letters.
- Aliases MUST be 3-5 character abbreviations derived from the table/entity name.

Examples: `dim_customer -> cust`, `dim_address -> addr`, `fact_sales_daily -> sales`, `fact_opportunity -> opp`.

## 3. SELECT Alias Matches INSERT Target

For `INSERT ... SELECT` statements, every selected expression MUST use `AS <TargetColumn>` and the alias MUST exactly match the corresponding target column name.

```sql
INSERT INTO silver.dim_customer (CustomerId, FirstName)
SELECT
    src.contactid AS CustomerId,
    src.firstname AS FirstName
FROM bronze.raw_d365_contact AS src;
```

## 4. CTEs Over Derived-Table Subqueries

Multi-step transformations MUST use named CTEs instead of nested derived-table subqueries.

## 5. Upsert Patterns

Use the following decision rules for Fabric Warehouse upserts:

| Scenario | Required / Allowed Pattern |
|---|---|
| Full refresh of a large table (>1M rows) | MUST use CTAS plus table swap |
| Distribution or index change | MUST use CTAS plus table swap |
| Incremental update affecting <20% of a table | MUST use DELETE + INSERT |
| Small dimension table (<100K rows) | MAY use MERGE or DELETE + INSERT |
| Atomic upsert semantics on a small table | MAY use MERGE |
| Table >100K rows | MERGE MUST NOT be the default; use CTAS or DELETE + INSERT unless an explicit project override authorizes MERGE |

MERGE in Fabric Warehouse MUST be treated as a concurrency-sensitive operation. Concurrent writes to the same target MUST be considered before selecting it.

## 6. SCD Type 2

An SCD Type 2 change MUST:

1. close the current row by setting its expiration date and `IsCurrent = 0`; and
2. insert the new current row with its effective date, open-ended expiration date, and `IsCurrent = 1`.

## 7. EXISTS / NOT EXISTS Reasoning

Every use of `EXISTS` or `NOT EXISTS` MUST have a nearby comment that states:

1. what existence condition is being tested; and
2. why `EXISTS` / `NOT EXISTS` is used instead of the relevant alternative.

## 8. Join Simplicity

- Business filters MUST be applied before joins in named CTEs.
- `JOIN ... ON` clauses MUST contain relationship predicates, not business-filter logic.
- `CASE` expressions and filter functions MUST NOT be embedded in join predicates.

## 9. Fabric Warehouse Rules

These rules apply to persisted Fabric Warehouse table columns unless stated otherwise.

### Data types

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

### CTAS output types

CTAS projections MUST explicitly cast expressions whose resulting type must be controlled, including aggregate outputs used as persisted columns.

### Batch loading

Repeated singleton `INSERT ... VALUES` statements MUST NOT be used for batch loads. Batch loads MUST use `INSERT ... SELECT`, CTAS, or `COPY INTO` as applicable.

### Schema evolution

If the required `ALTER COLUMN` operation is not supported by the target Fabric Warehouse capability, schema evolution MUST use a CTAS-and-swap pattern.

### Transactions

- Writes to the same target table MUST be serialized when concurrent writes would conflict.
- A transaction MUST contain only the statements required for the atomic operation; unrelated work MUST NOT be included in the same transaction.

### Query labels

ETL authoring queries MUST include an `OPTION (LABEL = '...')` label suitable for diagnostics.

### sqlcmd connections

- Fabric Warehouse `sqlcmd` calls MUST specify the database with `-d`.
- Fabric Warehouse connections MUST use Microsoft Entra authentication (`-G`); SQL authentication MUST NOT be used.

## 10. Header Comments

Every production SQL file MUST begin with a header comment containing:

- File
- Purpose
- Source
- Author
- Date
- Change Log

## 11. Production Validation

- Production SQL MUST NOT use `SELECT *`.
- Date-window filters used for repeatable ETL logic MUST use parameters rather than hard-coded run dates.
- Target-specific Fabric rules in section 9 MUST be applied only to Fabric Warehouse targets.

## 14. References (Non-Normative)

- Microsoft Fabric Skills for GitHub Copilot: <https://github.com/microsoft/skills-for-fabric>
- Microsoft Fabric SQLDW Authoring Skill: <https://github.com/microsoft/skills-for-fabric/tree/main/skills/sqldw-authoring-cli>
- Microsoft Fabric Medallion Architecture Skill: <https://github.com/microsoft/skills-for-fabric/tree/main/skills/e2e-medallion-architecture>

Sections 12 and 13 remain unassigned so existing section-reference numbering is not repurposed.
