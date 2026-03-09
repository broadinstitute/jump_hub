#!/usr/bin/env jupyter
# ---
# title: Explore JUMP profiles
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
# # Exploring JUMP Cell Painting Profiles
#
# This notebook demonstrates how to load and explore processed morphological profiles from the
# [JUMP Cell Painting](https://jump-cellpainting.broadinstitute.org/) dataset.
#
# It loads pre-processed, batch-corrected profiles directly from S3 — no local data or git clone needed.
#
# For more in-depth tutorials (metadata enrichment, activity scoring, image display, clustering),
# see the other notebooks on the [JUMP Hub](https://broadinstitute.github.io/jump_hub/).

# %% Imports
import pandas as pd
import plotly.express as px
import plotly.io as pio
import requests

pio.renderers.default = "png"  # Use "notebook_connected" for interactive plots

# %% [markdown]
# ## Load profile manifest
#
# The JUMP project publishes a versioned manifest that points to the latest processed profiles on S3.
# Each entry includes the dataset subset, the S3 URL, and links to the exact processing recipe used.
#
# Available subsets:
# - **crispr** / **orf** / **compound**: Standard (batch-corrected) profiles — recommended for most analyses
# - **crispr_interpretable** / **orf_interpretable** / **compound_interpretable**: Without batch correction, for feature interpretation

# %% Load manifest
INDEX_URL = "https://raw.githubusercontent.com/jump-cellpainting/datasets/v0.11.0/manifests/profile_index.json"

profile_index = requests.get(INDEX_URL).json()

for entry in profile_index:
    print(f"  {entry['subset']:>25s}: {entry['url'].split('/')[-1]}")

# %% [markdown]
# ## Load CRISPR profiles
#
# Let's load the CRISPR knockout dataset. These are well-level profiles with thousands of
# morphological features averaged over cells in each well.
#
# We'll read just a few columns first to keep things fast.

# %% Load CRISPR data
crispr_url = next(e["url"] for e in profile_index if e["subset"] == "crispr")

# Read metadata columns + a couple of features
columns = [
    "Metadata_Source",
    "Metadata_Plate",
    "Metadata_Well",
    "Metadata_JCP2022",
    "X_1",
    "X_2",
    "X_3",
]

crispr = pd.read_parquet(crispr_url, columns=columns)
print(f"Loaded {len(crispr):,} wells with {len(columns)} columns")
crispr.head()

# %% [markdown]
# ## Explore the data
#
# The `Metadata_JCP2022` column is the unique JUMP identifier for each perturbation.
# The `X_*` columns are batch-corrected morphological features (principal components, 1-indexed).
#
# Let's see how many unique perturbations and sources we have.

# %% Summary statistics
print(f"Unique perturbations: {crispr['Metadata_JCP2022'].nunique():,}")
print(f"Unique sources: {crispr['Metadata_Source'].nunique()}")
print(f"\nWells per source:")
print(crispr.groupby("Metadata_Source").size().to_string())

# %% [markdown]
# ## Visualize morphological features
#
# Plot the first two principal components, colored by data-generating source.
# Hover over points to see the JUMP perturbation ID.
#
# Since these profiles are batch-corrected, sources should be well-mixed
# (unlike the raw CellProfiler features in earlier versions of this notebook).

# %% Scatter plot
plot_data = crispr.sample(n=2000, random_state=42)

px.scatter(
    plot_data,
    x="X_1",
    y="X_2",
    color="Metadata_Source",
    hover_name="Metadata_JCP2022",
    title="CRISPR profiles: first two components",
    labels={"X_1": "Component 1", "X_2": "Component 2"},
)

# %% [markdown]
# ## Compare datasets
#
# Let's quickly compare the sizes of all three standard datasets.

# %% Dataset comparison
summary = []
for entry in profile_index:
    if entry["subset"] in ("crispr", "orf", "compound"):
        df = pd.read_parquet(entry["url"], columns=["Metadata_JCP2022"])
        summary.append({
            "dataset": entry["subset"],
            "wells": len(df),
            "unique_perturbations": df["Metadata_JCP2022"].nunique(),
        })

pd.DataFrame(summary)

# %% [markdown]
# ## Next steps
#
# This notebook covers the basics of loading and visualizing JUMP profiles.
# For deeper analysis, see the other tutorials on the [JUMP Hub](https://broadinstitute.github.io/jump_hub/):
#
# - **Add metadata**: Map JUMP IDs to gene names, compound structures, and perturbation types
# - **Calculate activity**: Score how strongly each perturbation affects cell morphology
# - **Display images**: View the original Cell Painting microscopy images
# - **Explore clusters**: Find perturbations with similar morphological profiles
