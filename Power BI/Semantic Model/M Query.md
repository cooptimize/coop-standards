---
id: powerbi_semantic_model_m_query
title: Power BI M Query
domain: powerbi
layer: semantic_model
artifact: m_query
technology: power_bi
status: active
---
# M Query

## Connection parameter standards

- Use `SQLServer` and `SQLDB` connection parameters.
- Do not use `PartialData` in new models.
- Define schema and table names as local query parameters.

```powerquery
let
    SchemaName = "sales",
    TableName = "Customer",
    Source = Sql.Database(SQLServer, SQLDB),
    Result = Source{[Schema = SchemaName, Item = TableName]}[Data]
in
    Result
```

## Development refresh standards

Use **Sync schema only** during development. Load imported data after deploying the semantic model.

## Fact query standards

`{Fact Table} Attributes` reads the source rows. Its paired `{Fact Table}` query is a one-row measure table containing one `Int64` column, `Calculation`, with value `0`.

Example: `Ledger Transaction Attributes` holds the data; `Ledger Transactions` holds measures.

## Measure table query standards

Use a literal `#table` for every one-row measure table so Tabular Editor can read it. Do not use the compressed `Binary.Decompress`/JSON expression produced by **Enter Data**.

```powerquery
#table(type table [Calculation = Int64.Type], {{0}})
```

## Power Query group-order standards

1. Parameters
2. Dimensions
3. Facts — Fact Measure Hosts, then Fact Attributes
4. Calculation Tables
5. Other Queries
