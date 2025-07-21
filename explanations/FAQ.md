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

### Which pipelines produced the latest datasets?

The [profiles_index.json](https://github.com/jump-cellpainting/datasets/blob/main/manifests/profile_index.json) file contains links to the specific version of the [jump profiling recipe](https://github.com/broadinstitute/jump-profiling-recipe) used and its configuration.

### Do we expect one gene’s JCP ID (JUMP Cell Painting ID) to be associated with multiple targets?

Yes, many genes are associated with multiple targets and are correctly annotated as such. For instance, `JCP2022_050797` (quinidine/quinine) has the targets `KCNK1` and `KCNN4`. Other genes are annotated as targeting genes in disparate families.

### Do JCP IDs within the compound dataset refer to the same compound?

Sometimes, two compounds were given separate JCP IDs because they had different names and `broad_sample` names. But after all of the data cleanup steps, they ended up being the same. Hence two different entries.

### Do JCP IDs within either the CRISPR or ORF datasets refer to the same gene?

In CRISPR, each JCP ID corresponds to a different gene. But in ORF there are frequently multiple reagents representing the same gene. In this case, we compute consensus profiles at the gene level by aggregating profiles by `Metadata_NCBI_Gene_ID` rather than by `Metadata_JCP2022`. This approach was selected after testing six different consensus strategies and evaluating their performance using phenotypic activity metrics ([private link](https://github.com/jump-cellpainting/morphmap/issues/178) | [html](https://zenodo.org/records/15699904/files/morphmap_consensus_profiles.html?download=1)).
