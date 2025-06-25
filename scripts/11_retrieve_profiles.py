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

# %% Imports
import polars as pl
import requests

# %% [markdown]
#
# The JUMP Cell Painting project provides several processed datasets for morphological profiling.
# Choose the dataset that matches your perturbation type:
#
# - **`crispr`**: CRISPR knockout genetic perturbations
# - **`orf`**: Open Reading Frame (ORF) overexpression perturbations
# - **`compound`**: Chemical compound perturbations
# - **`all`**: Combined dataset containing all perturbation types (use for cross-modality comparisons)
#
# Each dataset is available in two processing versions:
#
# - **Standard** (e.g., `crispr`, `compound`, `orf`): Fully processed including batch correction steps. **Recommended for most analyses** as they provide better cross-dataset comparability.
#
# - **Interpretable** (e.g., `crispr_interpretable`, `compound_interpretable`, `orf_interpretable`): Same initial processing but without batch correction transformations that modify the original feature space. Use these when you need to interpret individual morphological features.
#
# All datasets are stored as Parquet files on AWS S3 and can be accessed directly via their URLs.
#
# The index file below contains the **recommended profiles** for each subset. Each profile includes:
# - Direct links to the processing recipe and configuration used
# - ETags for data integrity verification
#
# For details on creating your own profile manifests, see the [manifest guide](https://github.com/broadinstitute/jump_hub/blob/main/howto/2_create_project_manifest.md).

# %% Paths
INDEX_FILE = "https://raw.githubusercontent.com/jump-cellpainting/datasets/main/manifests/profile_index.json"

# %% [markdown]
# We use the version-controlled manifest above to release the latest corrected profiles

# %%
# Load the JSON manifest
response = requests.get(INDEX_FILE)
profile_index = response.json()

# Display the manifest data
for dataset in profile_index:
    print(f"- {dataset['subset']}: {dataset['url']}")

# %% [markdown]
# Each profile in the manifest includes direct links to:
# - **recipe_permalink**: The exact version of the processing code used
# - **config_permalink**: The specific configuration file that defines the processing steps
#
# Let's display the key information from the manifest:

# %%
# Convert JSON to DataFrame for better display
profile_df = pl.DataFrame(profile_index)

# Show key information in a clean table
display_df = profile_df.select(
    [
        "subset",
        pl.col("url").str.extract(r"([^/]+)\.parquet$").alias("filename"),
        pl.col("recipe_permalink")
        .str.extract(r"tree/([^/]+)$")
        .str.slice(0, 7)
        .alias("recipe_version"),
        pl.col("config_permalink").str.extract(r"([^/]+)\.json$").alias("config"),
    ]
)
display_df

# %% [markdown]
# Let inspect the standard profiles.

# %%
# Create dictionary of subset -> url for the standard profiles only
filepaths = {
    dataset["subset"]: dataset["url"]
    for dataset in profile_index
    if dataset["subset"] in ("crispr", "orf", "compound")
}
print("Selected profiles:")
for subset, url in filepaths.items():
    print(f"  {subset}: {url.split('/')[-1]}")

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
