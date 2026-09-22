---
id: powerbi_semantic_model_relationships
title: Power BI Relationships
domain: powerbi
layer: semantic_model
artifact: relationship
technology: power_bi
status: active
---
# Relationships

## Model shape

- Use a star schema unless an approved project requirement overrides it.
- Keep dimensions flat; do not introduce relationship chains through intermediate dimension tables as the default shape.
- Relationships MUST define the fact table first and the dimension table second, with `N:1` cardinality.

## Keys

- Relationship key columns MUST use exact numeric types such as `int64` or `decimal`, not floating-point `double`.
- Hide relationship keys on the many side from report view.
- Set numeric relationship keys to `summarizeBy: none`.

## Filter direction

- Physical bidirectional relationships MUST NOT be the default.
- Use targeted `CROSSFILTER` in the applicable measure when temporary bidirectional propagation is required, unless an approved project override requires a physical bidirectional relationship.

## Inactive relationships

Every inactive relationship MUST have at least one intentional `USERELATIONSHIP()` consumer. Remove inactive relationships without a consumer.

## FKNULL relationships

An `FKNULL` relationship represents a fact-to-dimension relationship that does not and cannot conceptually exist. It MUST NOT replace a valid relationship whose key is unavailable, incomplete, or unmatched.

- Relate the fact table's `FKNULL` column to the dimension key.
- Create the relationship as active by default.
- Without a relationship, a dimension visual can repeat the fact result for every dimension member.
- With an active `FKNULL` relationship, the fact result is summarized under the dimension's blank/null member.
- Adding an `FKNULL` relationship after reports are deployed can change existing visual results. Treat it as a potentially breaking model change and regression-test affected reports before deployment.
