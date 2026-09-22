# Semantic Model Standards

Canonical Cooptimize semantic-model policy. DAX-expression authoring remains governed by `dax.md`.

## 1. Parameters

- Data-source connections MUST be parameter-driven. The standard connection parameters are `SQLServer`, `SQLDB`, and `PartialData` where applicable.
- Table and schema names used by a Power Query MUST be defined as local query parameters rather than repeated as inline literals.

## 2. Power Query Order

Power Query groups MUST appear in this order:

1. Parameters
2. Dimensions
3. Facts
   1. Fact Measure Tables
   2. Fact Attributes
4. Measure Tables
5. Other Queries

The prior screenshot-only rule has been converted to text. The screenshot is not required by this standard.

## 3. Fact and Measure Tables

- A fact with report-facing attributes MUST be split into a measure/fact table and a corresponding `{Fact Name} Attributes` table.
- A fact with no report-facing attributes MAY remain a single table.
- Report-authored measures MUST use the table name `Ad Hoc Report Measures`.
- Measures that span more than one fact MUST use `Multi-fact {Data Model Name} Measures`.
- The technical `Calculation` field in measure tables MUST be hidden.

## 4. Display Folders

Fact/attribute tables MUST use these folders where the corresponding fields exist:

- `Attributes`
- `Keys` - fields in this folder MUST be hidden.
- `Numbers` - fields in this folder MUST be hidden.

Date tables MUST use these folders where the corresponding fields exist:

- `Calendar`
- `Fiscal`
- `Relative`

## 5. Field and Measure Formatting

### Fields

- Integer and numeric columns that are not intended for aggregation MUST have summarization disabled.
- Date fields MUST use `mm/dd/yyyy`.
- Boolean/BIT fields MUST display `TRUE` / `FALSE`.
- Date/time values MUST be converted to the client's primary time zone.
- A converted date/time column name MUST identify the time zone, for example `Created Date ET`.
- Time-zone conversion MUST use SQL time-zone conversion logic. Fixed manual UTC offsets MUST NOT be used.

### Measures

- Whole-number measures MUST default to `#,###`.
- Percentage measures MUST use `##%` unless a project-specific format overrides it.
- Currency measures MUST use the canonical custom format `"$ #,0;–$ #,0;$ 0;--"` unless a project-specific currency format overrides it.
- If negative currency or percentage values are shown in parentheses and column alignment is required, the format MUST use a dynamic format with a non-breaking space rather than a trailing ordinary space.
- A plain trailing space MUST NOT be used to align positive/zero values.
- Aligned numeric displays that depend on this spacing MUST use regular Segoe UI; semibold/bold variants MUST NOT be used for those values because their number kerning differs.

Canonical dynamic currency example:

```dax
"$ #,0" & UNICHAR(160) & ";$ (#,0);$ 0" & UNICHAR(160)
```

## 6. Hierarchies and Sorting

- Fields that represent ordered levels MUST belong to a hierarchy.
- The first field in a hierarchy MUST be the field whose label can represent the hierarchy in visuals that do not allow the hierarchy name to be changed.
- String fields on the Date table MUST be sorted by an integer or Date sort column.
- Columns used only for sorting MUST be hidden.

## 7. KPI Presentation

KPI status indicators MUST use approved custom SVG assets rather than platform-default status icons.

## 8. Measures

- A filtered measure that extends an existing core measure MUST be named `{Core Measure} | {Filter}`, for example `Ledger Amount | Revenue`.
- A filtered measure MUST reference the existing core measure rather than duplicate the core aggregation logic.
- DAX syntax, expression structure, variables, filter behavior, and formatting discipline are governed by `dax.md`.

## 9. Composite Models

- Every composite-model family MUST designate exactly one `Primary` model.
- Shared dimensions MUST come from the Primary model.
- Secondary models MUST contribute add-on facts after the Primary model.
- Imported tables MUST NOT be renamed as part of composite-model assembly.

