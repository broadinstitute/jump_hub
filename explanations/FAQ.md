# Frequently Asked Questions

## Analyses

### How can I reproduce an environment to explore JUMP data?

The easiest way to set things up will be installing from pip in your environment of choice:

```
pip install jump-deps
```

## Data

### Does JUMP contain my compound/gene of interest?

The easiest way to find out is to follow the instructions on the perturbation availability  [section](https://broadinstitute.github.io/jump_hub/howto/interactive/0_overview.html#perturbation-availability). Alternatively, you can explore the [metadata tables](https://github.com/jump-cellpainting/datasets/tree/main/metadata) on the datasets repository, which are used to generate the explorable table.

### Where are the datasets' specifications?

The main resource to understand the technicalities of the JUMP datasets collection and assembly is on this [repo](https://github.com/jump-cellpainting/datasets).

### Why do some samples have images but no downstream analysis?

Some plates failed Quality Control (QC) but we kept them because they may be useful for developing QC methods.

### Why do some perturbations have so many replicates? 

Some genetic and chemical perturbations are positive or negative controls (see next question) and thus appear frequently in the dataset.

### What are the identifiers for positive and negative controls?

You can find all positive and negative controls for JUMP-ORF, -CRISPR, and -compound [here](https://lite.datasette.io/?url=https://zenodo.org/api/records/13255965/files/babel.db/content#/babel/babel?_filter_column=pert_type&_filter_op=contains&_filter_value=con&_sort=rowid).
For the compounds dataset the only negative control is 'JCP2022_033924' (DMSO). 
Most chemical compound plates contain 16 negative control wells, while some have as many as 28 wells. In the ORF dataset, replicates are positioned in wells O23, O24, P23 and P24. The remaining wells contain ORF treatments, with a single replicate of each per plate map and with five replicate plates produced per plate map ([private link](https://github.com/jump-cellpainting/megamap/issues/8#issuecomment-1413606031) | [html](https://zenodo.org/records/15699904/files/megamap_no_replicates.html?download=1)).

### What are the CellProfiler pipelines used to process images and output raw single cell level profiles for JUMP?

You can find the CellProfiler pipelines that perform illumination correction, segmentation and feature extraction [here](https://github.com/broadinstitute/imaging-platform-pipelines/tree/master/JUMP_production).

### What are the data analysis pipelines that convert raw profiles into well-level profiles?

There are two pipelines used: One converts single cell raw profiles into aggregated well level profiles, the second transforms these aggregated profiles to improve signal quality. We call the first pipeline `profiling-recipe` and it is located in [this](https://github.com/jump-cellpainting/profiling-recipe/tree/51a3a4b36814c0a721a2062928a703ea46c169c4) permalink. For the second pipeline, the [profiles_index.json](https://github.com/jump-cellpainting/datasets/blob/main/manifests/profile_index.json) file contains links to the specific version of the [jump profiling recipe](https://github.com/broadinstitute/jump-profiling-recipe) used and its configuration. To clarify, the `profiling-recipe` and `jump-profiling-recipe` are not the same, they correspond to the first and second pipelines, respectively.

### If processing one or more complete JUMP modalities, which version of the profiles should I use?

Several profile products are valid, but they answer different questions.

| Profile source                                                                        | Pros                                                                                                                            | Cons / when to be careful                                                                                                                                                                                         |
|---------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [Public JUMP manifest](https://github.com/jump-cellpainting/datasets/blob/v0.11.0/manifests/profile_index.json) (`jump-cellpainting/datasets`, e.g. `compound`, `orf`, `crispr`) | Best default for general JUMP analyses: Public, canonical, stable, and modality-specific.                                       | The public `compound` profile includes `source_7`, so it does not exactly match the final compound profile used for the JUMP production paper.                                                                    |
| Public [`all` profile](https://github.com/jump-cellpainting/datasets/blob/v0.11.0/manifests/profile_index.json#L44-L50)                                                                  | Convenient when comparing across ORF, CRISPR, and compound perturbations.                                                       | Larger and worse batch correction for users who only need one modality; it may be inconsistent with data generated from modality-specific profiles.                                         |
| CellProfiler features, [`compound_no_source7`](https://github.com/broadinstitute/jump_production/blob/1790d3623faae2626d7e1e99bed0442cf95bc925/manifests/profile_index.json#L44-L50)                                          | Use when reproducing or aligning with the JUMP production paper. It excludes `source_7`, which made batch correction difficult. | Compound-only and paper-specific; differs from the public all-source `compound` profile. Removing `source_7` changes the data and can change statistics.                                                          |
| [Production deep-learning profiles (`compound_DL_*`)](https://github.com/broadinstitute/jump_production/blob/1790d3623faae2626d7e1e99bed0442cf95bc925/manifests/profile_index.json#L2-L42)                                   | Useful only for analyses explicitly designed around those embeddings.                                                           | They are not the default CellProfiler profiles, are not CellProfiler morphology features, and should not be substituted for the `compound_no_source7` CellProfiler profile without documenting the analysis goal. |

Background discussion: [jump_hub PR #91](https://github.com/broadinstitute/jump_hub/pull/91#issuecomment-3993109928) and [monorepo issue #101](https://github.com/broadinstitute/monorepo/issues/101) track why the production-paper profile is `compound_no_source7`, how it relates to the interpretable companion profile, and why statistics must be recomputed when `source_7` is removed.

### Do we expect one gene’s JCP ID (JUMP Cell Painting ID) to be associated with multiple targets?

Yes, many genes are associated with multiple targets and are correctly annotated as such. For instance, `JCP2022_050797` (quinidine/quinine) has the targets `KCNK1` and `KCNN4`. Other genes are annotated as targeting genes in disparate families.

### Do JCP IDs within the compound dataset refer to the same compound?

Sometimes, two compounds were given separate JCP IDs because they had different names and `broad_sample` names. But after all of the data cleanup steps, they ended up being the same. Hence two different entries.

### Do JCP IDs within either the CRISPR or ORF datasets refer to the same gene?

In CRISPR, each JCP ID corresponds to a different gene. But in ORF there are frequently multiple reagents representing the same gene. In this case, we compute consensus profiles at the gene level by aggregating profiles by `Metadata_NCBI_Gene_ID` rather than by `Metadata_JCP2022`. This approach was selected after testing six different consensus strategies and evaluating their performance using phenotypic activity metrics ([private link](https://github.com/jump-cellpainting/morphmap/issues/178) | [html](https://zenodo.org/records/15699904/files/morphmap_consensus_profiles.html?download=1)).
