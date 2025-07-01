# Creating a Project Manifest

Have custom-processed JUMP profiles? Here's how to share them with others.

## Prerequisites

- Profiles processed using [jump-profiling-recipe](https://github.com/broadinstitute/jump-profiling-recipe/blob/main/DOCUMENTATION.md)
- A GitHub repository for your project
- AWS CLI configured (for S3 upload) or appropriate CLI for your cloud provider
- `jq` and `curl` installed

## Overview

You will create a manifest file that documents your processed profiles:


```json
{
    "datasets": [
        {
            "subset": "compound_no_source7",
            "url": "https://cellpainting-gallery.s3.amazonaws.com/cpg0042-chandrasekaran-jump/source_all/workspace/profiles_assembled/compound_no_source7/v1.0/profiles_var_mad_int_featselect_harmony.parquet",
            "recipe_permalink": "https://github.com/broadinstitute/jump-profiling-recipe/tree/v0.6.0",
            "config_permalink": "https://github.com/broadinstitute/2025_jump_addon_orchestrator/blob/a15dedb35383cb342cd010106615f99939178126/1.convert/input/compound_no_source7.json",
            "etag": ""
        },
        {
            "subset": "compound_no_source7_interpretable",
            "url": "https://cellpainting-gallery.s3.amazonaws.com/cpg0042-chandrasekaran-jump/source_all/workspace/profiles_assembled/compound_no_source7/v1.0/profiles_var_mad_int_featselect.parquet",
            "recipe_permalink": "https://github.com/broadinstitute/jump-profiling-recipe/tree/v0.6.0",
            "config_permalink": "https://github.com/broadinstitute/2025_jump_addon_orchestrator/blob/a15dedb35383cb342cd010106615f99939178126/1.convert/input/compound_no_source7.json",
            "etag": ""
        }
    ]
}
```

This manifest provides:

1. **Centralized profile registry** - All processed profile sets in one place
2. **Provenance tracking** - Recipe version and config file URLs enable reproducibility (Note: versioning of input files to the recipe would be needed for complete reproducibility, but that is outside the current system's scope)
3. **Standardized paths** - URLs follow the [Cell Painting Gallery folder structure](https://broadinstitute.github.io/cellpainting-gallery/data_structure.html) convention:
   - `source_all/workspace/profiles_assembled/` - Standard JUMP dataset path structure. The `source_all` is typically an institution identifier and should be present even if data is from a single source. While you may store data elsewhere, we recommend following this structure for compatibility.
   - `subset/` - Data description (compound_no_source7, orf_combined, crispr, etc.)
   - `version/` - Dataset version (v1.0, v1.1, v2.0, etc.)
   - `pipeline_filename.parquet` - Filename preserves the pipeline string (e.g., `profiles_var_mad_int_featselect_harmony.parquet`)


## Step-by-Step Guide

We'll use the [2024_Chandrasekaran_Production](https://github.com/jump-cellpainting/2024_Chandrasekaran_Production) project as an example, specifically the `compound_no_source7_interpretable` subset.

### Step 1: Define your dataset parameters

```bash
SUBSET="compound_no_source7"  # Descriptive name for this data subset
VERSION="v1.0"  # Dataset version 
PROFILES_FILE="profiles_var_mad_int_featselect_harmony.parquet"  # Final processed profiles
INTERPRETABLE_PROFILES_FILE="profiles_var_mad_int_featselect.parquet"  # Interpretable profiles
```

### Step 2: Upload your profiles to storage

This example shows uploading to S3, but adapt the commands for your storage location.

**Note for Cell Painting Gallery uploads:** Please follow the [contribution guidelines](https://broadinstitute.github.io/cellpainting-gallery/contributing_to_cpg.html) which will require creating a unique prefix (e.g., `cpg0042-chandrasekaran-jump`). 

```bash
aws s3 cp /path/to/${INTERPRETABLE_PROFILES_FILE} \
  s3://cellpainting-gallery/cpg0042-chandrasekaran-jump/source_all/workspace/profiles_assembled/${SUBSET}/${VERSION}/${INTERPRETABLE_PROFILES_FILE}

# Verify upload succeeded
aws s3 ls s3://cellpainting-gallery/cpg0042-chandrasekaran-jump/source_all/workspace/profiles/${SUBSET}/${VERSION}/ --human-readable
```

### Step 3: Create the manifest file

In your project repository, create `manifests/profile_index.json`:

```json
{
    "datasets": [
        {
            "subset": "compound_no_source7_interpretable",
            "url": "https://cellpainting-gallery.s3.amazonaws.com/cpg0042-chandrasekaran-jump/source_all/workspace/profiles/compound_no_source7/v1.0/profiles_var_mad_int_featselect.parquet",
            "recipe_permalink": "https://github.com/broadinstitute/jump-profiling-recipe/tree/v0.6.0",
            "config_permalink": "https://github.com/broadinstitute/2025_jump_addon_orchestrator/blob/a15dedb35383cb342cd010106615f99939178126/1.convert/input/compound_no_source7.json",
            "etag": ""
        }
    ]
}
```

**Note on recipe versioning:**

- If using a tagged version (e.g., `v0.6.0`), use the tag URL: `https://github.com/broadinstitute/jump-profiling-recipe/tree/v0.6.0`
- If using an untagged version, use the commit hash: `https://github.com/broadinstitute/jump-profiling-recipe/tree/522aa81cad73d5776f62745fd0cd19336d4cfff3`
- If using your own fork, point to your fork instead
- The goal is to provide a permanent link to the exact recipe version used 

### Step 4: Add ETags for data integrity

ETags are checksums that ensure data integrity when downloading. Use the automated script from the JUMP datasets repository.

Download the update_etags.sh script (check https://github.com/jump-cellpainting/datasets/tags for newer versions):

```bash
mkdir -p manifests/src
curl -o manifests/src/update_etags.sh https://raw.githubusercontent.com/jump-cellpainting/datasets/refs/tags/v0.10.0/manifests/src/update_etags.sh
```

Run the script to update ETags automatically:

```bash
bash manifests/src/update_etags.sh manifests/profile_index.json > manifests/profile_index.json.tmp && mv manifests/profile_index.json.tmp manifests/profile_index.json
```

The script automatically fetches and updates ETags for all URLs in your manifest. See the [README](https://github.com/jump-cellpainting/datasets/blob/main/manifests/src/README.md) for details.

### Step 5: Commit and push your manifest

```bash
git add manifests/profile_index.json
git commit -m "Add profile manifest"
git push
```

## Using Your Manifest

Your profiles are now documented and ready to share! See [`scripts/11_retrieve_profiles.py`](../scripts/11_retrieve_profiles.py) for an example of how to consume manifest files.

## Reference Examples

See these projects for reference implementations:
- [Main JUMP datasets](https://github.com/jump-cellpainting/datasets/blob/v0.10.0/manifests/profile_index.json)
- [2024_Chandrasekaran_Production](https://github.com/jump-cellpainting/2024_Chandrasekaran_Production/blob/main/manifests/profile_index.json)

