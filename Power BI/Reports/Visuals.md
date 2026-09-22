---
id: powerbi_reports_visuals
title: Power BI Report Visuals
domain: powerbi
layer: report
artifact: visual
technology: power_bi
status: active
---
# Report Visuals

Unless marked `MUST` or `MUST NOT`, these rules are defaults rather than requirements.  

## Layout

- Leave 16 pixels between visuals. At 100% zoom with snap to grid enabled, this is two grid movements.
- Use no alternating row color for small tables.
- Use alternating row color for large tables.
- Visual titles are centered and dark gray.

## Typography

Use Segoe UI by default. It provides the required flexibility and consistent numeric spacing; most other Power BI fonts are more limited.

## Color

- Use one primary color per visual.
- Use gray or lighter variations of the primary color for the remaining series and elements.
- Color MUST NOT be the only indicator of meaning. Combine colors and tints in charts, and combine color and shape in icons.
- Tables and matrices MUST NOT use cell shading.

## Chart selection

Select the chart type that best communicates the stated requirement.

## Interactions

- Chart interactions MUST use `Filter`, not `Highlight`.
- Drill-through pages MUST explicitly define their drill-through filters.

## Filters

- Use one to five visible slicers instead of relying on the built-in Filters pane. Slicers are easier to discover, offer more control over the user experience, and can be selectively synchronized across pages.
- Reports MUST NOT use bookmark-controlled filter panels. They require two bookmarks on every page and create unnecessary maintenance.

## KPIs

KPI status indicators MUST use approved custom SVG assets instead of platform-default status icons.
