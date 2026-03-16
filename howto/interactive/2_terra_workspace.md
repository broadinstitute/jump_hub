# Using JUMP data on Terra

[Terra](https://app.terra.bio) is a cloud-based platform for biomedical research. You can use Terra to explore JUMP Cell Painting data interactively via Jupyter notebooks in a cloud environment, without needing to set up a local computing environment.

## Overview

The JUMP Cell Painting dataset includes 116k chemical and >15k genetic perturbations (`cpg0016`), split across 12 data-generating centers, using human U2OS osteosarcoma cells. All data is hosted on the [Cell Painting Gallery](https://registry.opendata.aws/cellpainting-gallery/) on the Registry of Open Data on AWS.

The JUMP Hub [tutorial scripts](../../scripts/) fetch profiles via HTTP from the Cell Painting Gallery, so no local data or cloud credentials are needed — they work anywhere you can run a Jupyter notebook, including Terra.

## Prerequisites

- A [Terra](https://app.terra.bio) account with an active billing project.

## Running a tutorial on Terra

1. Create or open a workspace on Terra.
2. Start a cloud environment from the workspace. Recommended minimum settings:

    | Setting | Value |
    |---------|-------|
    | CPUs | 1 |
    | Disk Size | 50 GB |
    | Memory | 3.75 GB |

3. Pick a tutorial script from [`scripts/`](../../scripts/) and convert it to a notebook locally. For example, starting with [Retrieve JUMP profiles](../../scripts/11_retrieve_profiles.py):

    ```bash
    pip install jupytext
    jupytext --to notebook 11_retrieve_profiles.py
    ```

4. Upload the resulting `.ipynb` to the Terra workspace **Analyses** tab.
5. Open and run the notebook.

## About the data

- Most data components (images, raw CellProfiler output, single-cell profiles, aggregated CellProfiler profiles) are available from 12 sources for the principal dataset. Each source corresponds to a unique data-generating center (except `source_7` and `source_13`, which were from the same center).
- See [jump-cellpainting/datasets](https://github.com/jump-cellpainting/datasets) for full details on available and planned data releases.

## History

This guide was originally contributed by Nicole Deflaux (Verily) in March 2023 as part of the [datasets repository](https://github.com/jump-cellpainting/datasets/pull/55) and has been adapted for the JUMP Hub.
