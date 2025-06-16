#!/usr/bin/env jupyter
# ---
# title: Retrieve JUMP profiles
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.17.2
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# This is a tutorial on how to access profiles from the [JUMP Cell Painting datasets](https://github.com/jump-cellpainting/datasets).
# We will use polars to fetch the data frames lazily, with the help of `s3fs` and `pyarrow`.
# We prefer lazy loading because the data can be too big to be handled in memory.

# %% Imports
import polars as pl

# %% [markdown]
# ## JUMP Cell Painting Datasets & Recommendations
#
# The JUMP Cell Painting project provides several processed datasets for morphological profiling.
# Choose the dataset that matches your perturbation type:
#
# - **`crispr`**: CRISPR knockout genetic perturbations
# - **`orf`**: Open Reading Frame (ORF) overexpression perturbations
# - **`compound`**: Chemical compound perturbations
# - **`all`**: Combined dataset containing all perturbation types (use for cross-modality comparisons)
#
# ### Standard vs Interpretable Versions
#
# Each dataset is available in two processing versions:
#
# - **Standard** (e.g., `crispr`, `compound`, `orf`): Fully processed including batch correction steps. **Recommended for most analyses** as they provide better cross-dataset comparability.
#
# - **Interpretable** (e.g., `crispr_interpretable`, `compound_interpretable`, `orf_interpretable`): Same initial processing but without batch correction transformations that modify the original feature space. Use these when you need to interpret individual morphological features.
#
# All datasets are stored as Parquet files on AWS S3 and can be accessed directly via their URLs.
# Snakemake workflows for producing these assembled profiles are available [here](https://github.com/broadinstitute/jump-profiling-recipe/).
#
# To understand exactly how each profile was generated:
# 1. Extract the commit from the URL path (e.g., `jump-profiling-recipe_2024_a917fa7` → commit `a917fa7`)
# 2. Extract the pipeline string from the URL (the folder name after the subset, e.g., 
#    `ORF/profiles_wellpos_cc_var_mad_outlier_featselect_sphering_harmony/`)
# 3. In the repository at that commit, check the `inputs/` directory for configuration files:
#    - Individual subsets (orf/crispr/compound) → check orf.json, crispr.json, compound.json
#    - Combined "all" subsets → check pipeline_1.json, pipeline_2.json, pipeline_3.json
# 4. Find the config file where the "pipeline" value matches your pipeline string
#
# Note: "_interpretable" versions are intermediate files from the same pipeline, captured before 
# multivariate transformations like sphering or harmony. They use the same config but represent
# an earlier step in the processing pipeline (e.g., `profiles_wellpos_cc_var_mad_outlier_featselect`
# is the interpretable version before `_sphering_harmony` is applied).
#
# The index file below contains the **recommended profiles** for each subset:
#
# > **Note for maintainers**: Maintainers may consider adding project-specific custom profiles through separate index files as needed.

# %% Paths
INDEX_FILE = "https://raw.githubusercontent.com/jump-cellpainting/datasets/v0.9.0/manifests/profile_index.csv"

# %% [markdown]
# We use the version-controlled CSV above to release the latest corrected profiles

# %%
profile_index = pl.read_csv(INDEX_FILE)

profile_index

# %% [markdown]
# The processing pipeline applied to each dataset is encoded directly in the parquet file names.
# The filename shows the sequence of processing steps that were applied, as defined in the
# [JUMP profiling recipe documentation](https://github.com/broadinstitute/jump-profiling-recipe/blob/main/DOCUMENTATION.md).
#
# Key pipeline steps include:
# - `profiles`: Base profiles (initial data loading)
# - `var`: Variance thresholding - dropping features with very low variability
# - `mad`: Robust standardization - normalizing features so that controls on each plate have a mean of 0 and a standard deviation of 1
# - `int`: Inverse Normal Transformation - transforming feature distributions to be more normally distributed
# - `featselect`: Feature selection - various methods to select features including reducing features to the most diverse ones
# - `harmony`: Harmony batch correction - removing technical variations between batches (this is the default)
#
# Let's extract and display the pipeline information from the file names:

# %%
pl.Config.set_fmt_str_lengths(200)
display_df = profile_index.with_columns(
    pl.col("url").str.extract(r"([^/]+)\.parquet$").alias("pipeline")
).select("subset", "pipeline")
display_df

# %%
pl.Config.set_fmt_str_lengths(50)

# %% [markdown]
# We do not need the 'etag' (used to check file integrity) column nor the 'interpretable' (i.e., before major modifications)

# %%
selected_profiles = profile_index.filter(
    pl.col("subset").is_in(("crispr", "orf", "compound"))
).select(pl.exclude("etag"))
filepaths = dict(selected_profiles.iter_rows())
print(filepaths)

# %% [markdown]
# We will lazy-load the dataframes and print the number of rows and columns

# %%
info = {k: [] for k in ("dataset", "#rows", "#cols", "#Metadata cols", "Size (MB)")}
for name, path in filepaths.items():
    data = pl.scan_parquet(path)
    n_rows = data.select(pl.len()).collect().item()
    schema = data.collect_schema()
    metadata_cols = [col for col in schema.keys() if col.startswith("Metadata")]
    n_cols = schema.len()
    n_meta_cols = len(metadata_cols)
    estimated_size = int(round(4.03 * n_rows * n_cols / 1e6, 0))  # B -> MB
    for k, v in zip(info.keys(), (name, n_rows, n_cols, n_meta_cols, estimated_size)):
        info[k].append(v)

pl.DataFrame(info)

# %% [markdown]
# Let us now focus on the `crispr` dataset and use a regex to select the metadata columns.
# We will then sample rows and display the overview.
# Note that the collect() method enforces loading some data into memory.

# %%
data = pl.scan_parquet(filepaths["crispr"])
data.select(pl.col("^Metadata.*$").sample(n=5, seed=1)).collect()

# %% [markdown]
# The following line excludes the metadata columns:

# %%
data_only = data.select(pl.all().exclude("^Metadata.*$").sample(n=5, seed=1)).collect()
data_only

# %% [markdown]
# Finally, we can convert this to `pandas` if we want to perform analyses with that tool.
# Keep in mind that this loads the entire dataframe into memory.

# %%
data_only.to_pandas()
