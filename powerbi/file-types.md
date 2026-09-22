---
id: powerbi_file_types
title: Power BI File Types
domain: powerbi
layer: agnostic
artifact: file_type
technology: power_bi
status: active
---
# Choosing a Power BI File Type

## Selection

| Source control | Required format |
|---|---|
| OneDrive or SharePoint | PBIX |
| Git | PBIP with PBIR |

- OneDrive and SharePoint workflows MUST use PBIX. Microsoft supports only PBIX files in the Power BI Desktop OneDrive/SharePoint integration.
- Git workflows MUST use PBIP with PBIR so report and semantic-model definitions are stored as reviewable text files.
- PBIX MUST NOT be the canonical Git artifact. Git can store the binary, but it does not provide useful diffs or merges.
- PBIP MUST NOT be used for a OneDrive or SharePoint workflow.

## PBIP and PBIR

- PBIP is the project container for the report and semantic model.
- PBIR is the report definition format inside the project; it is not an alternative to PBIP.
- PBIR stores pages, visuals, bookmarks, and report metadata as separate JSON files under the report's `definition/` folder.
- The semantic model in a PBIP project MUST use TMDL.

## Enhanced report format preview

Microsoft's **Store reports using enhanced metadata format (PBIR)** preview option enables PBIR. It replaces the legacy `report.json` representation with the `definition/` folder.

- New Git projects MUST enable PBIR.
- Conversion of an existing PBIR-Legacy project MUST be explicitly approved for that project because Power BI Desktop cannot reverse the upgrade through its UI.
- Preview limitations MUST be reviewed before conversion or deployment.
- Enabling PBIR inside a PBIX does not make the PBIX source-control friendly and is not required for OneDrive or SharePoint workflows.

## References (non-normative)

- [Power BI Desktop project report folder](https://learn.microsoft.com/power-bi/developer/projects/projects-report)
- [Power BI Desktop OneDrive and SharePoint integration](https://learn.microsoft.com/power-bi/create-reports/desktop-sharepoint-save-share)
