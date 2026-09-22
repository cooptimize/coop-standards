---
id: tech_fabric_performance
title: Fabric Warehouse Execution and Performance
domain: sql
layer: agnostic
artifact: agnostic
technology: fabric_warehouse
status: active
---
# Fabric Warehouse Execution and Performance Standards

Applies only to statements executed against Fabric Warehouse, including statements inside stored procedures. These requirements do not select an incremental-loading or upsert implementation.

## Concurrent writes

Writes to the same target table MUST be serialized when concurrent writes would conflict.

MERGE in Fabric Warehouse MUST be treated as a concurrency-sensitive operation. Concurrent writes to the same target MUST be considered before selecting it.

## Transaction scope

A transaction MUST contain only the statements that must commit together; unrelated work MUST NOT be included.

## Diagnostics

ETL authoring queries MUST include an `OPTION (LABEL = '...')` label suitable for diagnostics.
