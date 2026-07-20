## Quirks and details

There are additional details that are not commonly asked but it is important to retain on record. This is a compendium of those.

### Experimental-source details

- `source_1` and `source_9` use higher-density plates (1536 vs. the standard 384-well format).
- `source_7` and `source_13` are the same laboratory.
- In JUMP-Target there is an InChIKey that maps to 2 different perturbations: `LOUPRKONTZGTKE-UHFFFAOYSA-N` maps to both quinidine and quinine.
- The definition of controls, especially positive controls, can be tricky: Some are hard-coded in [broad_babel](https://github.com/broadinstitute/monorepo/blob/febe56c27e490c110d8b5a871de974a4293176c6/libs/jump_babel/tools/gen_database.py#L70-L87), based on internal knowledge that was not recorded at the time of assembling the datasets. In certain datasets, such as JUMP-ORF, there are additional types of positive controls: `poscon_orf`, `poscon_cp` (compound probe), and `poscon_diverse`.
- The treatment compounds were assayed at 10 uM for all sources, except for `source_7` where the compounds were assayed at 0.625 uM (the goal being to assay some of the compounds at a low concentration in addition to the higher concentration used for most of data production). The positive control compounds in compound, ORF and CRISPR plates were assayed at 5 uM. JUMP-Target-1-Compound and JUMP-Target-2-Compound plates were also assayed at 5 uM.
- Due to some plates having letters and numbers and others only numbers, be careful when loading multiple `load_data_csv`s. We treat all columns as strings to avoid any potential casting issue.

### Choosing among profile sources and manifests

Several profile products are valid, but they answer different questions. Do not silently swap between them: cosine similarities, feature ranks, activity p-values, and downstream JUMPrr tables should be regenerated whenever the input profile changes.

| Profile source | Pros | Cons / when to be careful |
| --- | --- | --- |
| Public JUMP manifest (`jump-cellpainting/datasets`, e.g. `compound`, `orf`, `crispr`) | Best default for general JUMP analyses and JUMP Hub tutorials; public, canonical, stable, and modality-specific. | The public `compound` profile includes `source_7`, so it does not exactly match the final compound profile used for the JUMP production paper. |
| Public `all` profile | Convenient when ORF, CRISPR, and compound perturbations need to live in one dataframe, especially for cross-modality comparisons. | Larger and more cognitively noisy for users who only need one modality; can become inconsistent with tools or tables that were generated from modality-specific profiles. |
| Production-paper CellProfiler profile, `compound_no_source7` | Use when reproducing or aligning with the JUMP production paper and related JUMPrr tables. It excludes `source_7`, which made batch correction difficult, and is the final CellProfiler compound profile identified in the production manifest. The associated activity statistics were recalculated for this profile. | Compound-only and paper-specific; differs from the public all-source `compound` profile. Removing `source_7` changes the data and can change statistics, so do not reuse p-values or feature tables computed from all-source profiles. |
| `compound_no_source7_interpretable` companion profile | Useful when strict pre-Harmony CellProfiler feature names/values are needed. It also provides the positional feature-name mapping for `compound_no_source7` (`X_1`...`X_758` map to the 758 CellProfiler features in the same order). | Not the batch-corrected profile used for matching in the production-paper workflow. For JUMPrr feature tables, a separate interpretable input is not necessarily required because the Harmony profile can be positionally renamed, but the values are still Harmony-corrected. |
| Production deep-learning profiles (`compound_DL_*`) | Useful only for analyses explicitly designed around those embeddings. | They are not the default CellProfiler profiles, are less directly interpretable as CellProfiler morphology features, and should not be substituted for the `compound_no_source7` CellProfiler profile without documenting the analysis goal. |

Background discussion: [jump_hub PR #91](https://github.com/broadinstitute/jump_hub/pull/91#issuecomment-3993109928) and [monorepo issue #101](https://github.com/broadinstitute/monorepo/issues/101) track why the production-paper profile is `compound_no_source7`, how it relates to the interpretable companion profile, and why statistics must be recomputed when `source_7` is removed.
