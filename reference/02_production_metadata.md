# JUMP production metadata

The JUMP production [augmented metadata database](https://imaging-platform.s3.amazonaws.com/projects/cpg0042-chandrasekaran-jump/workspace/publication_data/2025_Chandrasekaran/jump_production_datastore/interim/jump_metadata_augmented.duckdb) is the source for the compound target and mechanism-of-action (MoA) annotations used in the JUMP production analysis. These are annotations of compounds, not annotations of the corresponding genetic perturbations.

## Database contents

The DuckDB database combines:

- core JUMP metadata for compounds, ORF and CRISPR perturbations, plates, wells, controls, and microscope configurations;
- Drug Repurposing Hub compound names, targets, MoAs, clinical phases, diseases, and indications;
- ChEMBL, Chemical Probes, and MOTIVE compound-target annotations;
- ToxCast, toxicity, pharmacokinetic, MitoTox, chemical-property, and cell-count annotations.

The `compound_metadata` view provides one row per JUMP compound and joins the fields most commonly needed for analysis, including the JUMP ID, InChIKey, chemical structure, targets, and MoAs.

## Attach the database with DuckDB

Open the [DuckDB Web Shell](https://shell.duckdb.org/) or start a local DuckDB CLI session, then run:

```sql
INSTALL httpfs;
LOAD httpfs;

ATTACH 'https://imaging-platform.s3.amazonaws.com/projects/cpg0042-chandrasekaran-jump/workspace/publication_data/2025_Chandrasekaran/jump_production_datastore/interim/jump_metadata_augmented.duckdb'
    AS meta (READ_ONLY);

DESCRIBE meta.compound_metadata;
```

The database remains remote and is attached read-only as the `meta` catalog. Tables and views can then be queried with names such as `meta.compound_metadata`, `meta.compound`, and `meta.repurposing_hub_annotations`.

## Query compound annotations

Drug Repurposing Hub MoA annotations are available in `Metadata_repurposing_moa`. This example retrieves compounds annotated as HSP inhibitors:

```sql
SELECT "Metadata_JCP2022" AS jump_id,
       "Metadata_InChIKey" AS inchikey,
       "Metadata_repurposing_name" AS compound_name
FROM meta.compound_metadata
WHERE 'HSP inhibitor' IN (
    SELECT trim(x)
    FROM UNNEST(string_split("Metadata_repurposing_moa", '|')) AS t(x)
);
```

Chemical Probes target genes are available in `Metadata_chmprb_target_genes`. This example retrieves the compounds associated with `HSP90AA1`, together with their Drug Repurposing Hub MoA when available:

```sql
SELECT "Metadata_JCP2022" AS jump_id,
       "Metadata_InChIKey" AS inchikey,
       "Metadata_repurposing_name" AS compound_name,
       "Metadata_repurposing_moa" AS mechanism_of_action
FROM meta.compound_metadata
WHERE 'HSP90AA1' IN (
    SELECT trim(x)
    FROM UNNEST(string_split("Metadata_chmprb_target_genes", '|')) AS t(x)
);
```

Replace `HSP inhibitor` or `HSP90AA1` with the exact MoA or target label of interest. The annotations can contain pipe-delimited lists; splitting those lists and testing exact membership avoids false matches between similarly named targets.
