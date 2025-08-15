#!/usr/bin/env jupyter
# ---
# title: Available genes in JUMP
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.16.4
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---
# %% [markdown]
# Is my gene of interest in JUMP or other associated datasets? We provide a [tutorial](https://broadinstitute.github.io/jump_hub/howto/interactive/1_jumprr_steps.html#was-my-gene-tested-in-the-jump-collection-of-perturbations) with details.
#
# The number in the table indicates how many copies are present (it is mostly 0's and 1's, but there are some genes that correspond to multiple JUMP ids). Note that the JUMP columns include all genes, whereas the PERISCOPE ones (A549, Hela_X) include the hits only (statistically significant). The Lacoste dataset contains all entries.
#
# This table was generated using [this](https://github.com/broadinstitute/jump_hub/blob/main/tools/create_gene_coverage_table.py) script.
#
# %%
# | code-fold: true
import polars as pl
import pooch
from itables import show

logger = pooch.get_logger()
logger.setLevel("WARNING")
df = pl.read_csv(
    pooch.retrieve(
        f"https://zenodo.org/api/records/16882914/files/table.csv/content",
        known_hash="135654ca760699a2e69378cf59021efc1ed8a03e0870be312e0283d68c1523b3",
    )
)
show(df, maxBytes=0)
