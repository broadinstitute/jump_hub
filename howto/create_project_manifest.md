# Creating a Project Manifest

Have custom-processed JUMP profiles? Here's how to share them with others.

**Note**: This guide describes the recommended approach for new projects. Some existing datasets may use different URL structures with metadata embedded in paths.

## Prerequisites

- Processed profiles from [jump-profiling-recipe](https://github.com/broadinstitute/jump-profiling-recipe/blob/main/DOCUMENTATION.md)
- AWS CLI configured (for S3 upload)
- A GitHub repository for your project

## URL Structure with Manifest-Based Provenance

Store your processed profiles using semantic paths with versioning metadata tracked in the manifest:

```
https://s3.amazonaws.com/bucket/project/data/subset/version/profiles.parquet
```

**Components:**
- `data/` - Indicates processed profile data
- `subset/` - Data description (compound_no_source7, orf_combined, crispr, etc.)
- `version/` - Dataset version (v1.0, v1.1, v2.0, etc.)
- `profiles.parquet` - Standard filename for processed profiles

**Approach:**
- **Semantic paths** organize data by subset and version for easy navigation
- **Independent versioning** allows you to version different subsets separately
- **Manifest-based provenance** captures all processing details without embedding them in paths
- **GitHub permalinks** provide permanent references to exact code and configuration

**Provenance Tracking:**
Processing details (recipe version, config, commit) are captured in the manifest using GitHub permalinks that provide permanent links to the exact code and configuration used.

## Working Example

Here's a complete example:

**Repository Setup:**
- Project repo: `jump-cellpainting/2024_Chandrasekaran_Production`
- Processing repo: `broadinstitute/jump-profiling-recipe` at commit `598189f`
- Config used: `inputs/config/compound.json`

**S3 URLs:**
```
# Final processed version (v1.0)
https://cellpainting-gallery.s3.amazonaws.com/cpg0042-chandrasekaran-jump/data/compound_no_source7/v1.0/profiles.parquet

# Interpretable version (v1.0)  
https://cellpainting-gallery.s3.amazonaws.com/cpg0042-chandrasekaran-jump/data/compound_no_source7_interpretable/v1.0/profiles.parquet
```

**Manifest with provenance:**
```csv
"subset","url","etag","recipe_permalink","config_permalink"
"compound_no_source7","https://cellpainting-gallery.s3.amazonaws.com/cpg0042-chandrasekaran-jump/data/compound_no_source7/v1.0/profiles.parquet","35cb79ad41b1a4eb9afeab0d90035dfa-330","https://github.com/broadinstitute/jump-profiling-recipe/tree/598189f","https://github.com/broadinstitute/jump-profiling-recipe/blob/598189f/inputs/config/compound.json"
"compound_no_source7_interpretable","https://cellpainting-gallery.s3.amazonaws.com/cpg0042-chandrasekaran-jump/data/compound_no_source7_interpretable/v1.0/profiles.parquet","3ece1cc202c4a2190e84a95a2dd2d6b3-418","https://github.com/broadinstitute/jump-profiling-recipe/tree/598189f","https://github.com/broadinstitute/jump-profiling-recipe/blob/598189f/inputs/config/compound.json"
```

## Steps

### 1. Upload to S3

Upload your profiles using semantic paths:

```bash
# Get commit hash from your jump-profiling-recipe for provenance tracking
cd /path/to/jump-profiling-recipe
COMMIT=$(git rev-parse --short HEAD)
echo "Using commit: $COMMIT"

# Set variables for your specific case
SUBSET="compound_no_source7"  # Descriptive name for your data 
VERSION="v1.0"  # Dataset version (v1.0, v1.1, etc.)

# Upload to semantic path:
aws s3 cp /path/to/your/profiles.parquet \
  s3://your-bucket/your-project/data/${SUBSET}/${VERSION}/profiles.parquet

# For interpretable version (if you have both files):
aws s3 cp /path/to/your/profiles_interpretable.parquet \
  s3://your-bucket/your-project/data/${SUBSET}_interpretable/${VERSION}/profiles.parquet

# Verify upload succeeded
aws s3 ls s3://your-bucket/your-project/data/ --recursive --human-readable
```

**Note:** Replace `/path/to/your/` with your actual file location, `your-bucket` and `your-project` with your actual S3 bucket and project names.

### 2. Create manifest in your project repo

In your project repository, create the directory structure:

```bash
mkdir -p manifests
```

Create `manifests/profile_index.csv` with GitHub permalinks for provenance:

```csv
"subset","url","etag","recipe_permalink","config_permalink"
"compound_no_source7","https://s3.amazonaws.com/your-bucket/your-project/data/compound_no_source7/v1.0/profiles.parquet","","https://github.com/broadinstitute/jump-profiling-recipe/tree/598189f","https://github.com/broadinstitute/jump-profiling-recipe/blob/598189f/inputs/config/compound.json"
"compound_no_source7_interpretable","https://s3.amazonaws.com/your-bucket/your-project/data/compound_no_source7_interpretable/v1.0/profiles.parquet","","https://github.com/broadinstitute/jump-profiling-recipe/tree/598189f","https://github.com/broadinstitute/jump-profiling-recipe/blob/598189f/inputs/config/compound.json"
```

**Replace with your values:**
- `your-bucket/your-project` - Your actual S3 bucket and project names
- `598189f` - Your actual commit hash from Step 1
- `compound.json` - Your actual config file used
- `compound_no_source7` - Your actual subset name

### 3. Add ETags for data integrity

ETags are checksums that ensure data integrity when downloading:

```bash
# Get ETag for each file (replace with your actual URLs)
curl -I https://s3.amazonaws.com/your-bucket/your-project/data/compound_no_source7/v1.0/profiles.parquet | grep ETag

# Example output: 
# ETag: "d41d8cd98f00b204e9800998ecf8427e-1"
```

Update your CSV with the ETag values:

```csv
"subset","url","etag","recipe_permalink","config_permalink"
"compound_no_source7","https://s3.amazonaws.com/your-bucket/your-project/data/compound_no_source7/v1.0/profiles.parquet","d41d8cd98f00b204e9800998ecf8427e-1","https://github.com/broadinstitute/jump-profiling-recipe/tree/598189f","https://github.com/broadinstitute/jump-profiling-recipe/blob/598189f/inputs/config/compound.json"
"compound_no_source7_interpretable","https://s3.amazonaws.com/your-bucket/your-project/data/compound_no_source7_interpretable/v1.0/profiles.parquet","a71b2c3d4e5f6789abcdef1234567890-2","https://github.com/broadinstitute/jump-profiling-recipe/tree/598189f","https://github.com/broadinstitute/jump-profiling-recipe/blob/598189f/inputs/config/compound.json"
```

### 4. Commit and push

```bash
git add manifests/profile_index.csv
git commit -m "Add profile manifest"
git push
```

### 5. Use your manifest

Now anyone can use your profiles with full provenance tracking:

```python
# In any analysis script
import polars as pl

INDEX_FILE = "https://raw.githubusercontent.com/your-org/your-project/main/manifests/profile_index.csv"
profile_index = pl.read_csv(INDEX_FILE)

# Users can now access both data and provenance:
# - profile_index["url"] - Data URLs
# - profile_index["recipe_permalink"] - Exact processing code
# - profile_index["config_permalink"] - Exact configuration used

# Continue with standard retrieval process
# ... follow scripts/11_retrieve_profiles.py workflow
```

**Benefits for users:**
- **Organized URLs** - structured by subset and version for easy navigation
- **Complete reproducibility** - permalinks to exact code and config
- **Version tracking** - can identify dataset versions  
- **Permanent links** - GitHub permalinks never change

## Example Projects

See these projects for reference:
- [Main JUMP datasets](https://github.com/jump-cellpainting/datasets/blob/main/manifests/profile_index.csv) - the standard pattern
- [2024_Chandrasekaran_Production](https://github.com/jump-cellpainting/2024_Chandrasekaran_Production/blob/main/manifests/profile_index.csv) - compound data example
- Your project manifest will follow the same structure

Compare your manifest format to these examples to ensure compatibility.

## Need to Process Data First?

See the [jump-profiling-recipe documentation](https://github.com/broadinstitute/jump-profiling-recipe/blob/main/DOCUMENTATION.md) for processing instructions.