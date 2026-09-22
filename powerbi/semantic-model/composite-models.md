---
id: powerbi_semantic_model_composite_models
title: Power BI Composite Models
domain: powerbi
layer: semantic_model
artifact: composite_model
technology: power_bi
status: active
---
# Composite Models

- Every composite-model family MUST designate exactly one `Primary` model.
- Shared dimensions MUST come from the Primary model.
- Secondary models MUST contribute add-on facts after the Primary model.
- Imported tables MUST retain their source names during composite-model assembly.

`Finance + Project Accounting` uses Finance as Primary and Project Accounting as an add-on. SIOP uses Inventory as Primary and Project Management as an add-on.

## Large dimensions

Large or high-cardinality dimensions, such as Voucher, can cause model-size and memory errors in composite models.

- These dimensions MUST NOT be included in a composite model by default.
- A required large dimension MUST be validated for model size, memory use, and successful deployment before adoption.

## Open decisions (non-normative)

- Whether Production participates in the SIOP composite model.
