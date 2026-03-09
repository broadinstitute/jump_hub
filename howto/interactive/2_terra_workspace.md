# Using JUMP data on Terra

[Terra](https://app.terra.bio) is a cloud-based platform for biomedical research, operated by the Broad Institute and Verily. You can use Terra to explore JUMP Cell Painting data interactively via Jupyter notebooks in a cloud environment, without needing to set up a local computing environment.

## Overview

The JUMP Cell Painting dataset includes 116k chemical and >15k genetic perturbations (`cpg0016`), split across 12 data-generating centers, using human U2OS osteosarcoma cells. All data is hosted on the [Cell Painting Gallery](https://registry.opendata.aws/cellpainting-gallery/) on the Registry of Open Data on AWS.

The [Explore JUMP profiles](../../scripts/17_explore_profiles.py) tutorial notebook fetches batch-corrected profiles via HTTP from the Cell Painting Gallery, so no local data or cloud credentials are needed — it works anywhere you can run a Jupyter notebook, including Terra.

## Prerequisites

<!-- TODO: Confirm Terra account details — is it free for all academics? Are there cloud compute costs beyond the free tier? -->
- A [Terra](https://app.terra.bio) account with an active billing project.

## Running the notebook on Terra

1. Create or open a workspace on Terra.
2. Start a cloud environment from the workspace. Recommended minimum settings:

    | Setting | Value |
    |---------|-------|
    | CPUs | 1 |
    | Disk Size | 50 GB |
    | Memory | 3.75 GB |

3. Download the [Jupytext script](../../scripts/17_explore_profiles.py) and convert it to a notebook locally:

    ```bash
    pip install jupytext
    jupytext --to notebook 17_explore_profiles.py
    ```

4. Upload the resulting `17_explore_profiles.ipynb` to the Terra workspace **Analyses** tab.
5. Open and run the notebook. It reads profiles directly from S3 — no additional data setup is required.

## About the data

- Most data components (images, raw CellProfiler output, single-cell profiles, aggregated CellProfiler profiles) are available from 12 sources for the principal dataset. Each source corresponds to a unique data-generating center (except `source_7` and `source_13`, which were from the same center).
- See [jump-cellpainting/datasets](https://github.com/jump-cellpainting/datasets) for full details on available and planned data releases.

## History

This guide was originally contributed by Nicole Deflaux (Verily) in March 2023 as part of the [datasets repository](https://github.com/jump-cellpainting/datasets/pull/55) and has been adapted for the JUMP Hub.
