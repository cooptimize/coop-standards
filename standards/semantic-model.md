<!-- ASSEMBLED from structured articles by scripts/assemble.py.
     Edit the source article under SQL/, Power BI/, or Technology/ and re-run
     `python3 scripts/assemble.py`. Do not hand-edit sections here. -->

# Choosing a Power BI File Type

## File selection standards

| Workflow | Required format |
|---|---|
| OneDrive or SharePoint | PBIX |
| Git | PBIP with PBIR |

Do not use PBIP for OneDrive/SharePoint workflows or PBIX as the canonical Git artifact. PBIX is binary and does not provide useful diffs or merges.

## Project format standards

- PBIP contains the report and semantic model; use TMDL for the model.
- PBIR defines the report inside that project. It stores pages, visuals, bookmarks, and report metadata as separate JSON files under `definition/`.

```text
Report/definition/pages/…
```

## Enhanced report format standards

- Enable PBIR for new Git projects through **Store reports using enhanced metadata format (PBIR)**.
- Get explicit project approval before converting PBIR-Legacy: Desktop cannot reverse the upgrade through its UI.
- Review preview limitations before conversion or deployment.
- PBIR replaces the legacy `report.json` representation. Enabling it inside a PBIX does not make that binary file useful for Git and is not required for OneDrive/SharePoint.

## PBIP Git exclusions

Exclude local data caches and per-user settings from Git. Check these entries even when `.gitignore` already exists; Desktop only creates the file when one is absent.

```gitignore
**/.pbi/localSettings.json
**/.pbi/cache.abf
```

Do not ignore the entire `.pbi` folder: it can also contain shared project settings. Adding ignore rules does not remove files already tracked by Git; untrack those files while retaining local copies.

## References (non-normative)


- [Power BI Desktop project report folder](https://learn.microsoft.com/power-bi/developer/projects/projects-report)
- [Power BI Desktop OneDrive and SharePoint integration](https://learn.microsoft.com/power-bi/create-reports/desktop-sharepoint-save-share)
- [Microsoft: PBIP files and default Git exclusions](https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-overview)
- [Microsoft: semantic-model project files](https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-dataset)

# Power BI App Deployment

## Standards

### App logo standards

Create workspace and app logos in Canva: select an existing icon and apply the report theme colors.

## Default positions

### Workspace audience defaults

Organize workspaces by department or user group. The workspace represents the audience.

### App audience defaults

Avoid dividing an app into Power BI audiences; the management overhead is rarely worth it.

# Report Page Formatting

## Standards

### Report theme standards

Use a theme file in every report.

### Visual background standards

Use white visual backgrounds.

## Default positions

### Report palette defaults

Start with the customer's primary logo or website colors and build the palette from them.

### Report page defaults

- Use a 16:9 HD page, 1920 × 1080.
- Use a very light gray page background.
- Use a slightly darker gray canvas background.

# Report Visuals

## Standards

### Visual accessibility standards

- Never use color alone to convey meaning. Combine color and tint in charts, and color and shape in icons.
- Never use table or matrix cell shading.

### Visual interaction standards

- Set chart interactions to **Filter**, not **Highlight**.
- Explicitly define drill-through filters.
- Do not create bookmark-controlled filter panels: they require two bookmarks on every page.

### KPI standards

Use approved custom SVG assets for KPI status indicators instead of platform-default status icons.

## Default positions

### Visual layout defaults

- Leave 16 pixels between visuals: two grid movements at 100% zoom with snap to grid enabled.
- Center titles and use dark gray.
- Choose charts for the reporting requirement.
- Use Segoe UI for flexibility and consistent numeric spacing.

### Visual color defaults

- Use one primary color per visual; use gray or lighter variations for other elements.
- Small tables have no alternating row colors. Large tables use alternating row colors.

### Slicer defaults

Use one to five visible slicers instead of relying on the built-in Filters pane. Slicers are discoverable, flexible, and can be selectively synchronized across pages.

## Open decisions (non-normative)

Clarify whether the cell-shading prohibition excludes alternating row backgrounds, which are the current default for large tables.

# M Query

## Connection parameter standards

- Use `SQLServer` and `SQLDB` connection parameters.
- Do not use `PartialData`, the legacy development data-limiting parameter, in new models.
- Define schema and table names as local `let` steps, distinct from the shared `SQLServer` and `SQLDB` parameters.

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

In Power BI Desktop, expand **Home > Refresh** and choose **Sync schema only** during development. Load imported data after deploying the semantic model.

## Fact query standards

For a split fact, the Attributes query reads source rows. Its paired measure query contains one `Int64` column, `Calculation`, and one row with value `0`.

Example: `Ledger Transaction Attributes` holds the data; `Ledger Transactions` holds measures.

Table placement and visibility are defined in [Fact Tables](<Fact Tables.md>).

## Measure table query standards

Use a literal `#table` for every one-row measure table so Tabular Editor can read it. Do not use the compressed `Binary.Decompress`/JSON expression produced by **Enter Data**.

```powerquery
#table(type table [Calculation = Int64.Type], {{0}})
```

## Power Query group-order standards

1. Parameters
2. Dimensions
3. Facts — Fact Measure Hosts, then Fact Attributes
4. Calculation Tables — the `Ad Hoc Calculations` and `Multi-Fact Calculations` measure tables, not calculation groups or DAX calculated tables
5. Other Queries — supporting queries and functions outside the groups above

## Open decisions (non-normative)

- A migration process for existing `PartialData` models is not defined.
- Allowed M transformations, native queries, and query-folding requirements are not defined. Do not infer a ban on all M transformations from the simple source-navigation example.
- Power BI incremental-refresh parameters and setup are not defined here; loading recipes belong in the separate patterns knowledge base.

## References (non-normative)

- [Microsoft: Power BI refresh options](https://learn.microsoft.com/en-us/power-bi/connect-data/refresh-data)

# Composite Models

## Standards

### Composite model structure standards

- Designate exactly one Primary model in each composite-model family.
- Take shared dimensions from Primary; add facts from secondary models afterward.
- Keep imported table names unchanged.

`Finance + Project Accounting`: Finance is Primary; Project Accounting adds facts. For SIOP, Inventory is Primary and Project Management adds facts.

### Large dimension validation standards

When a large or high-cardinality dimension such as Voucher is required, validate model size, memory use, and successful deployment before adopting it.

## Default positions

### Composite dimension defaults

Exclude large or high-cardinality dimensions such as Voucher by default; they can cause model-size and memory errors.

## Open decisions (non-normative)

Whether Production participates in SIOP.

# Fact Measure and Attribute Tables

## Fact table structure standards

- A fact with report-facing attributes uses a source-backed Attributes table and a paired one-row measure table named for the fact.
- Keep fields in Attributes and measures in the measure table.
- A fact without report-facing attributes can remain one source-backed table and be split later.

| Table | Contents |
|---|---|
| Ledger Transaction Attributes | Source rows and fields |
| Ledger Transactions | One-row table holding measures |

## Calculation table standards

- Put measures associated with one fact in its measure table.
- Every model includes `Ad Hoc Calculations` for measures authored inside reports, primarily for testing.
- Put measures spanning facts that do not belong to a single fact's measure table in `Multi-Fact Calculations`.
- Hide the technical `Calculation` field in every measure table.

## Fact display-folder standards

Use these folders when the fields exist:

| Folder | Visibility |
|---|---|
| Attributes | Report-facing fields |
| Keys | All fields hidden |
| Numbers | All fields hidden |

## Open decisions (non-normative)

- A universal singular/plural naming rule is not defined; `Ledger Transaction Attributes` and `Ledger Transactions` are the approved example.
- Whether one-row measure tables must remain disconnected is not explicitly defined. Do not infer a relationship requirement from the phrase "one-row table."

# Relationships

## Standards

### Relationship key standards

- Define the fact first and dimension second, with `N:1` cardinality.
- Use `int64` relationship keys, hide them, and set summarization to none.

```text
Sales[FKCustomer] → Customer[PKCustomer] (N:1)
```

### Inactive relationship standards

Every inactive relationship needs an intentional `USERELATIONSHIP()` consumer. Remove inactive relationships with no consumer.

```dax
USERELATIONSHIP(FactSales[FKShipDate], 'Date'[PKDate])
```

### FKNULL relationship standards

Use `FKNULL` only when the fact and dimension cannot conceptually be joined. Never use it to replace a valid relationship with missing, incomplete, or unmatched keys.

Relate the fact's `FKNULL` column to the dimension key. Without a relationship, a visual can repeat the fact result for each dimension member. An active `FKNULL` relationship summarizes it under the blank/null member.

Adding this after deployment can change report results. Regression-test affected reports before deployment.

```text
Sales[FKNULL] → UnrelatedDimension[PKDimension] (N:1)
```

## Default positions

### Model shape defaults

Use a star schema with flat dimensions. Avoid chains through intermediate dimension tables unless an approved project requirement overrides this shape.

### Filter direction defaults

Avoid physical bidirectional relationships. Use `CROSSFILTER` in the measure when temporary bidirectional filtering is needed, unless an approved project override requires a physical relationship.

### FKNULL activation defaults

Make `FKNULL` relationships active.

# Organizing Semantic Model Tables

## Table naming standards

- Use PascalCase table and calculated-column names.
- Qualify column references with the table name.

```dax
Customer[CustomerGroup]
```

## Field formatting standards

- Disable summarization for numeric columns not intended for aggregation.
- Format dates as `mm/dd/yyyy` and Boolean/BIT fields as `TRUE` / `FALSE`.
- Convert timestamps to the client's primary time zone in SQL using time-zone conversion, never a fixed UTC offset.
- Show the local date, time, and zone; include the zone in the column name.

```text
Created Date ET: 10/06/2025 3:00 PM Eastern
```

## Date table standards

- Use one contiguous, marked Date table for time intelligence.
- Disable auto date/time and remove `LocalDateTable_*` and `DateTableTemplate_*` tables.
- Use `Calendar`, `Fiscal`, and `Relative` folders when those fields exist.

## Dimension folder standards

Dimension folders are optional. When used, group fields by subject.

## Hierarchy and sorting standards

- Put ordered levels in a hierarchy with a clear name.
- Put first the field whose label can represent the hierarchy in visuals where it cannot be renamed.
- Sort Date-table strings by an integer or Date column. Hide sort-only columns.

```text
Month Name → sort by Month Number (hidden)
```

## Semantic model deployment standards

- Do not use unsupported calculated columns in Direct Lake models.
- Direct Lake table names match their source exactly.
- Deploy semantic-model source with TMDL, not TMSL.

## Open decisions (non-normative)

Clarify the scope of PascalCase naming: approved measure-table names and report-facing column names contain spaces, and Direct Lake tables retain source names.
