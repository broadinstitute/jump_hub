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
# - **Standard** (e.g., `crispr`, `compound`, `orf`): Fully processed including batch correction steps. **Recommended for most analyses** as they provide better cross-dataset comparability and have undergone additional quality control.
#
# - **Interpretable** (e.g., `crispr_interpretable`, `compound_interpretable`, `orf_interpretable`): Same initial processing but without batch correction transformations that modify the original feature space. Use these when you need to interpret individual morphological features or understand the biological meaning of specific measurements.
#
# All datasets are stored as Parquet files on AWS S3 and can be accessed directly via their URLs.
# Snakemake workflows for producing these assembled profiles are available [here](https://github.com/broadinstitute/jump-profiling-recipe/).
# The specific commit used to produce the profiles can be found in the folder path of each parquet file.
# For example, `jump-profiling-recipe_2024_a917fa7` indicates commit `a917fa7` was used.
#
# The index file below contains the **recommended profiles** for each subset:
#
# > **Note for future**: Project-specific custom profiles will be available through separate index files as needed.

# %% Paths
INDEX_FILE = "https://raw.githubusercontent.com/jump-cellpainting/datasets/v0.9.0/manifests/profile_index.csv"

# %% [markdown]
# We use the version-controlled CSV above to release the latest corrected profiles

# %%
profile_index = pl.read_csv(INDEX_FILE)
profile_index

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
