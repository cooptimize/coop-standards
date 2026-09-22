---
id: tech_fabric_warehouse
title: Fabric Warehouse Target
domain: sql
layer: agnostic
artifact: agnostic
technology: fabric_warehouse
status: active
---
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
