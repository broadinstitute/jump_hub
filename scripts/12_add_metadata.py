#!/usr/bin/env jupyter
# ---
# title: Add metadata to profiles
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
# A very common task when processing morphological profiles is knowing which ones are treatments and which ones are controls.
# Here we will explore how we can use broad-babel to accomplish this task.

# %% Imports
import polars as pl
import requests
from broad_babel.query import get_mapper

# %% [markdown]
# We will be using the CRISPR dataset specificed in our json index file.

# %% Fetch the CRISPR dataset
INDEX_FILE = "https://raw.githubusercontent.com/jump-cellpainting/datasets/v0.11.0/manifests/profile_index.json"
response = requests.get(INDEX_FILE)
profile_index = response.json()

CRISPR_URL = (
    pl.DataFrame(profile_index).filter(pl.col("subset") == "crispr").item(0, "url")
)
profiles = pl.scan_parquet(CRISPR_URL)
print(profiles.collect_schema().names()[:6])

# %% [markdown]
# For simplicity the contents of our processed profiles are minimal: "The profile origin" (source, plate and well) and the unique JUMP identifier for that perturbation. We will use broad-babel to further expand on this metadata, but for simplicity's sake let us sample subset of data.

# %% Subset data
jcp_ids = (
    profiles.select(pl.col("Metadata_JCP2022")).unique().collect().to_series().sort()
)
subsample = jcp_ids.sample(10, seed=42)
# Add a well-known control
subsample = (*subsample, "JCP2022_800002")
subsample

# %% [markdown]
# We will use these JUMP ids to obtain a mapper that indicates the perturbation type (trt, negcon or, rarely, poscon)

# %% Pull mapper
pert_mapper = get_mapper(
    subsample, input_column="JCP2022", output_columns="JCP2022,pert_type"
)
pert_mapper

# %% [markdown]
# A couple of important notes about broad_babel's get mapper and other functions:
# - these must be fed tuples, as these are cached and provide significant speed-ups for repeated calls
# - 'get-mapper' works for datasets for up to a few tens of thousands of samples. If you try to use it to get a mapper for the entirety of the 'compounds' dataset it is likely to fail. For these cases we suggest the more general function 'run_query'. You can read more on this and other use-cases on Babel's [readme](https://github.com/broadinstitute/monorepo/tree/main/libs/jump_babel).
#
# We will now repeat the process to get their 'standard' name

# %% Fetch standard name
name_mapper = get_mapper(
    (*subsample, "JCP2022_800002"),
    input_column="JCP2022",
    output_columns="JCP2022,standard_key",
)
name_mapper

# %% [markdown]
# To wrap up, we will fetch all the available profiles for these perturbations and use the mappers to add the missing metadata. We also select a few features to showcase how how selection can be performed in polars.

# %% Filter profiles and merge metadata
subsample_profiles = profiles.filter(
    pl.col("Metadata_JCP2022").is_in(subsample)
).collect()
profiles_with_meta = subsample_profiles.with_columns(
    pl.col("Metadata_JCP2022").replace(pert_mapper).alias("pert_type"),
    pl.col("Metadata_JCP2022").replace(name_mapper).alias("name"),
)
profiles_with_meta.select(
    pl.col(("name", "pert_type", "^Metadata.*$", "^X_[0-3]$"))
).sort(by="pert_type")
