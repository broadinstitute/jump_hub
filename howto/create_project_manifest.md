# Creating a Project Manifest

Have custom-processed JUMP profiles? Here's how to share them with others.

## Prerequisites

- Processed profiles from [jump-profiling-recipe](https://github.com/broadinstitute/jump-profiling-recipe/blob/main/DOCUMENTATION.md)
- AWS CLI configured (for S3 upload)
- A GitHub repository for your project

## URL Structure for Reproducibility

Your manifest URLs should follow the JUMP dataset convention with workspace nesting:

```
https://s3.amazonaws.com/bucket/project/source_all/workspace/profiles/FORK_jump-profiling-recipe_YEAR_COMMIT/SUBSET/pipeline_directory/filename.parquet
```

**Components:**
- `FORK_jump-profiling-recipe_YEAR_COMMIT` - Fork owner, tool name, year, and commit hash
- `SUBSET/` - Data description (COMPOUND, ORF, CRISPR, compound_no_source7, orf_combined, etc.)
- `pipeline_directory/` - The exact pipeline string used
- `filename.parquet` - Final output file (may differ from pipeline name)

**Important:** The pipeline directory name and actual filename may differ:
- Pipeline directory: `profiles_var_mad_int_featselect_harmony`
- Harmony file: `profiles_var_mad_int_featselect_harmony.parquet`  
- Interpretable file: `profiles_var_mad_int_featselect.parquet`

This allows others to:
1. Extract the fork and commit: `username_jump-profiling-recipe_2024_a1b2c3d` → `username/jump-profiling-recipe` at commit `a1b2c3d`
2. Extract the pipeline: `profiles_var_mad_int_featselect_harmony`
3. Find the config: Check `inputs/config/` in that specific fork at that commit
4. Match the pipeline: Find the config file where `"pipeline"` matches your string

## Working Example

Here's a complete example from the 2024_Chandrasekaran_Production project:

**Repository Setup:**
- Project repo: `jump-cellpainting/2024_Chandrasekaran_Production`
- Processing repo: `broadinstitute/jump-profiling-recipe` at commit `598189f`
- Data type: Compound profiles without source 7

**Variables:**
```bash
FORK_OWNER="broadinstitute"
COMMIT="598189f" 
YEAR="2024"
SUBSET="compound_no_source7"  # Descriptive name for this specific dataset
PIPELINE="profiles_var_mad_int_featselect_harmony"
```

**Final S3 URLs:**
```
# Final processed version
https://cellpainting-gallery.s3.amazonaws.com/cpg0042-chandrasekaran-jump/source_all/workspace/profiles/jump-profiling-recipe_2024_598189f/compound_no_source7/profiles_var_mad_int_featselect_harmony/profiles_var_mad_int_featselect_harmony.parquet

# Interpretable version  
https://cellpainting-gallery.s3.amazonaws.com/cpg0042-chandrasekaran-jump/source_all/workspace/profiles/jump-profiling-recipe_2024_598189f/compound_no_source7/profiles_var_mad_int_featselect_harmony/profiles_var_mad_int_featselect.parquet
```

**Final manifest:**
```csv
"subset","url","etag"
"compound_no_source7","https://cellpainting-gallery.s3.amazonaws.com/cpg0042-chandrasekaran-jump/source_all/workspace/profiles/jump-profiling-recipe_2024_598189f/compound_no_source7/profiles_var_mad_int_featselect_harmony/profiles_var_mad_int_featselect_harmony.parquet","35cb79ad41b1a4eb9afeab0d90035dfa-330"
"compound_no_source7_interpretable","https://cellpainting-gallery.s3.amazonaws.com/cpg0042-chandrasekaran-jump/source_all/workspace/profiles/jump-profiling-recipe_2024_598189f/compound_no_source7/profiles_var_mad_int_featselect_harmony/profiles_var_mad_int_featselect.parquet","3ece1cc202c4a2190e84a95a2dd2d6b3-418"
```

## Steps

### 1. Upload to S3

Make your profiles publicly accessible using a structured path that includes processing provenance:

```bash
# Get the fork owner and commit hash from your jump-profiling-recipe
cd /path/to/jump-profiling-recipe
FORK_OWNER=$(git remote get-url origin | sed 's/.*github\.com[:/]\([^/]*\)\/.*/\1/')  # Extract GitHub username
COMMIT=$(git rev-parse --short HEAD)
echo "Using fork: $FORK_OWNER, commit: $COMMIT"

# Set variables for your specific case
YEAR=$(date +%Y)  # Current year, or use the year you processed the data
SUBSET="compound_no_source7"  # Descriptive name for your data 
PIPELINE="profiles_var_mad_int_featselect_harmony"  # Your actual pipeline string

# Upload to workspace path (cellpainting-gallery pattern):
aws s3 cp /path/to/your/${PIPELINE}.parquet \
  s3://your-bucket/your-project/source_all/workspace/profiles/jump-profiling-recipe_${YEAR}_${COMMIT}/${SUBSET}/${PIPELINE}/${PIPELINE}.parquet

# For interpretable version (if you have both files):
INTERPRETABLE_FILE="profiles_var_mad_int_featselect.parquet"  # Adjust filename as needed
aws s3 cp /path/to/your/${INTERPRETABLE_FILE} \
  s3://your-bucket/your-project/source_all/workspace/profiles/jump-profiling-recipe_${YEAR}_${COMMIT}/${SUBSET}/${PIPELINE}/${INTERPRETABLE_FILE}

# Verify upload succeeded
aws s3 ls s3://your-bucket/your-project/ --recursive --human-readable | grep ${COMMIT}
```

**Note:** Replace `/path/to/your/` with your actual file location, `your-bucket` and `your-project` with your actual S3 bucket and project names.

### 2. Create manifest in your project repo

In your project repository, create the directory structure:

```bash
mkdir -p manifests
```

Create `manifests/profile_index.csv` (replace with your actual URLs from Step 1):

```csv
"subset","url","etag"
"compound","https://s3.amazonaws.com/your-bucket/your-project/source_all/workspace/profiles/username_jump-profiling-recipe_2024_a1b2c3d/COMPOUND/profiles_var_mad_int_featselect_harmony/profiles_var_mad_int_featselect_harmony.parquet",""
"compound_interpretable","https://s3.amazonaws.com/your-bucket/your-project/source_all/workspace/profiles/username_jump-profiling-recipe_2024_a1b2c3d/COMPOUND/profiles_var_mad_int_featselect_harmony/profiles_var_mad_int_featselect.parquet",""
```

**Note**: Replace `username_jump-profiling-recipe_2024_a1b2c3d` with your actual fork owner, year and commit hash, `COMPOUND` with your data description (can be any descriptive name like `compound_subset1`, `orf_combined`, etc.), and the pipeline strings with your actual processing pipeline.

### 3. Add ETags for data integrity

ETags are checksums that ensure data integrity when downloading:

```bash
# Get ETag for each file (replace with your actual URLs)
curl -I https://s3.amazonaws.com/your-bucket/your-project/.../your-file.parquet | grep ETag

# Example output: 
# ETag: "d41d8cd98f00b204e9800998ecf8427e-1"
```

Update your CSV with the ETag values:

```csv
"subset","url","etag"
"compound","https://s3.amazonaws.com/your-bucket/your-project/source_all/workspace/profiles/username_jump-profiling-recipe_2024_a1b2c3d/COMPOUND/profiles_var_mad_int_featselect_harmony/profiles_var_mad_int_featselect_harmony.parquet","d41d8cd98f00b204e9800998ecf8427e-1"
"compound_interpretable","https://s3.amazonaws.com/your-bucket/your-project/source_all/workspace/profiles/username_jump-profiling-recipe_2024_a1b2c3d/COMPOUND/profiles_var_mad_int_featselect_harmony/profiles_var_mad_int.parquet","a71b2c3d4e5f6789abcdef1234567890-2"
"orf","https://s3.amazonaws.com/your-bucket/your-project/source_all/workspace/profiles/username_jump-profiling-recipe_2024_a1b2c3d/ORF/profiles_wellpos_cc_var_mad_outlier_featselect/profiles_wellpos_cc_var_mad_outlier_featselect.parquet","b82c3d4e5f6789abcdef1234567890a7-3"
```

### 4. Commit and push

```bash
git add manifests/profile_index.csv
git commit -m "Add profile manifest"
git push
```

### 5. Use your manifest

Now anyone can use your profiles:

```python
# In any analysis script
INDEX_FILE = "https://raw.githubusercontent.com/your-org/your-project/main/manifests/profile_index.csv"

# Then use the standard retrieval process
import polars as pl
profile_index = pl.read_csv(INDEX_FILE)
# ... continue with scripts/11_retrieve_profiles.py workflow
```

## Example Projects

See these projects for reference:
- [Main JUMP datasets](https://github.com/jump-cellpainting/datasets/blob/main/manifests/profile_index.csv) - the standard pattern
- [2024_Chandrasekaran_Production](https://github.com/jump-cellpainting/2024_Chandrasekaran_Production/blob/main/manifests/profile_index.csv) - compound data example
- Your project manifest will follow the same structure

Compare your manifest format to these examples to ensure compatibility.

## Need to Process Data First?

See the [jump-profiling-recipe documentation](https://github.com/broadinstitute/jump-profiling-recipe/blob/main/DOCUMENTATION.md) for processing instructions.