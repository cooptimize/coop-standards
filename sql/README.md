# SQL Standards

`standards.yml` selects active SQL articles by layer, artifact, and technology.

## Scope

- Gold SQL uses `formatting.md`, one artifact article under `gold/`, and the selected target articles under `../tech/`.
- Gold table retrieval MUST select `fact_table` or `dimension_table`; there is no generic table route.
- Bronze and Silver are generated deterministically. The Silver route documents that boundary and may hold verified generator behavior and human-approved indexing rules; it does not instruct an LLM to author layer output. Bronze has no active article yet.
- Approved indexing rules for Bronze or Silver belong in directly routed articles and must be implemented by the deterministic process. No additional Bronze or Silver index policy is approved here.
- General performance guidance belongs to its separate knowledge base.
- Incremental loading, upsert selection, SCD implementation, and batch-loading recipes belong to the separate patterns knowledge base.

For example, `standards.yml` directly loads `formatting.md`, `gold/views.md`, and `../tech/fabric/warehouse.md` for a Gold view on Fabric Warehouse. Article text does not define retrieval dependencies.

`../deprecation/sql.md` is unchanged historical material and is excluded from active retrieval.
