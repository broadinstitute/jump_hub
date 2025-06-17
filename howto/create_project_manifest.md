# Creating a Project Manifest

Have custom-processed JUMP profiles? Here's how to share them with others.

**Note**: This guide describes the recommended approach for new projects. Some existing datasets may use different URL structures with metadata embedded in paths. While existing JUMP manifests use CSV format, we now recommend JSON for new projects due to its flexibility and structure.

## Prerequisites

- Processed profiles from [jump-profiling-recipe](https://github.com/broadinstitute/jump-profiling-recipe/blob/main/DOCUMENTATION.md)
- AWS CLI configured (for S3 upload)
- A GitHub repository for your project

## URL Structure with Manifest-Based Provenance

Store your processed profiles using semantic paths with versioning metadata tracked in the manifest:

```
https://s3.amazonaws.com/bucket/project/source_all/workspace/profiles/subset/version/pipeline_filename.parquet
```

**Components:**
- `source_all/workspace/profiles/` - Standard JUMP dataset path structure
- `subset/` - Data description (compound_no_source7, orf_combined, crispr, etc.)
- `version/` - Dataset version (v1.0, v1.1, v2.0, etc.)
- `pipeline_filename.parquet` - Filename preserves the pipeline string (e.g., `profiles_var_mad_int_featselect_harmony.parquet`)

**Approach:**
- **Semantic paths** organize data by subset and version for easy navigation
- **Independent versioning** allows you to version different subsets separately
- **Manifest-based provenance** captures all processing details without embedding them in paths
- **GitHub permalinks** provide permanent references to exact code and configuration

**Provenance Tracking:**
Processing details (recipe version, config, commit) are captured in the manifest using GitHub permalinks that provide permanent links to the exact code and configuration used.

## Steps

We'll walk through creating a manifest for the 2024_Chandrasekaran_Production project as an example.

### 1. Upload to S3

Upload your profiles using semantic paths:

```bash
# Note the version/commit of jump-profiling-recipe used
# For the Chandrasekaran example, we used v0.6.0

# Set variables for the Chandrasekaran example
SUBSET="compound_no_source7"  # Descriptive name for this data subset
VERSION="v1.0"  # Dataset version 
PROFILES_FILE="profiles_var_mad_int_featselect_harmony.parquet"  # Final processed profiles
INTERPRETABLE_PROFILES_FILE="profiles_var_mad_int_featselect.parquet"  # Interpretable profiles

# Upload to semantic paths:
aws s3 cp /path/to/${PROFILES_FILE} \
  s3://cellpainting-gallery/cpg0042-chandrasekaran-jump/source_all/workspace/profiles/${SUBSET}/${VERSION}/${PROFILES_FILE}

aws s3 cp /path/to/${INTERPRETABLE_PROFILES_FILE} \
  s3://cellpainting-gallery/cpg0042-chandrasekaran-jump/source_all/workspace/profiles/${SUBSET}/${VERSION}/${INTERPRETABLE_PROFILES_FILE}

# Verify upload succeeded
aws s3 ls s3://cellpainting-gallery/cpg0042-chandrasekaran-jump/source_all/workspace/profiles/ --recursive --human-readable
```

This creates the final URLs:
```
https://cellpainting-gallery.s3.amazonaws.com/cpg0042-chandrasekaran-jump/source_all/workspace/profiles/compound_no_source7/v1.0/profiles_var_mad_int_featselect_harmony.parquet
https://cellpainting-gallery.s3.amazonaws.com/cpg0042-chandrasekaran-jump/source_all/workspace/profiles/compound_no_source7/v1.0/profiles_var_mad_int_featselect.parquet
```

### 2. Create manifest in your project repo

In your project repository, create the directory structure:

```bash
mkdir -p manifests
```

Create `manifests/profile_index.json` for the Chandrasekaran example:

```json
{
    "datasets": [
        {
            "subset": "compound_no_source7",
            "url": "https://cellpainting-gallery.s3.amazonaws.com/cpg0042-chandrasekaran-jump/source_all/workspace/profiles/compound_no_source7/v1.0/profiles_var_mad_int_featselect_harmony.parquet",
            "recipe_permalink": "https://github.com/broadinstitute/jump-profiling-recipe/tree/v0.6.0",
            "config_permalink": "https://github.com/broadinstitute/2025_jump_addon_orchestrator/blob/a15dedb35383cb342cd010106615f99939178126/1.convert/input/compound_no_source7.json",
            "etag": ""
        },
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

The permalinks provide complete provenance - linking to the exact recipe version and config file used.

### 3. Add ETags for data integrity

ETags are checksums that ensure data integrity when downloading:

```bash
# Get ETag for each file
curl -I https://cellpainting-gallery.s3.amazonaws.com/cpg0042-chandrasekaran-jump/source_all/workspace/profiles/compound_no_source7/v1.0/profiles_var_mad_int_featselect_harmony.parquet | grep ETag

# Example output: 
# ETag: "35cb79ad41b1a4eb9afeab0d90035dfa-330"
```

Insert the ETag values into your JSON manifest from Step 2.

### 4. Commit and push

```bash
git add manifests/profile_index.json
git commit -m "Add profile manifest"
git push
```

### 5. Use your manifest

Your Chandrasekaran project manifest is now ready for use:

```python
# In any analysis script
import requests

INDEX_FILE = "https://raw.githubusercontent.com/jump-cellpainting/2024_Chandrasekaran_Production/main/manifests/profile_index.json"
manifest = requests.get(INDEX_FILE).json()

# Access data and provenance for each dataset:
for dataset in manifest["datasets"]:
    print(dataset["subset"], dataset["url"])
    # dataset["recipe_permalink"] - Exact processing code
    # dataset["config_permalink"] - Exact configuration used

# Continue with standard retrieval process
# ... follow scripts/11_retrieve_profiles.py workflow
```

This provides complete reproducibility while organizing data by subset and version.

## Example Projects

See these projects for reference:
- [Main JUMP datasets](https://github.com/jump-cellpainting/datasets/blob/main/manifests/profile_index.csv) - uses CSV format (legacy)
- [2024_Chandrasekaran_Production](https://github.com/jump-cellpainting/2024_Chandrasekaran_Production/blob/main/manifests/profile_index.json) - uses JSON format (recommended)

Note: Existing projects may still use CSV format. New projects should use JSON as shown in this guide.

## Need to Process Data First?

See the [jump-profiling-recipe documentation](https://github.com/broadinstitute/jump-profiling-recipe/blob/main/DOCUMENTATION.md) for processing instructions.