# Creating a Project Manifest

Have custom-processed JUMP profiles? Here's how to share them with others.

## Prerequisites

- Processed profiles from [jump-profiling-recipe](https://github.com/broadinstitute/jump-profiling-recipe/blob/main/DOCUMENTATION.md)
- AWS CLI configured (for S3 upload)
- A GitHub repository for your project

## URL Structure for Reproducibility

Your manifest URLs should follow the JUMP dataset convention to ensure full reproducibility. Following the [JUMP dataset pattern](../scripts/11_retrieve_profiles.py), your URLs should encode:

```
https://s3.amazonaws.com/bucket/project/profiles/FORK_jump-profiling-recipe_YEAR_COMMIT/SUBSET/pipeline_directory/filename.parquet
```

**Components:**
- `username_jump-profiling-recipe_2024_a1b2c3d` - Fork owner, tool name, year, and commit hash
- `SUBSET/` - Data type (COMPOUND, ORF, CRISPR, etc.)
- `pipeline_directory/` - The exact pipeline string used
- `filename.parquet` - Final output file

This allows others to:
1. Extract the fork and commit: `username_jump-profiling-recipe_2024_a1b2c3d` → `username/jump-profiling-recipe` at commit `a1b2c3d`
2. Extract the pipeline: `profiles_var_mad_int_featselect_harmony`
3. Find the config: Check `inputs/config/` in that specific fork at that commit
4. Match the pipeline: Find the config file where `"pipeline"` matches your string

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
SUBSET="COMPOUND"  # Change to ORF, CRISPR, etc. based on your data type
PIPELINE="profiles_var_mad_int_featselect_harmony"  # Your actual pipeline string

# Upload with structured path including fork and commit info
aws s3 cp outputs/compound/${PIPELINE}.parquet \
  s3://your-bucket/your-project/profiles/${FORK_OWNER}_jump-profiling-recipe_${YEAR}_${COMMIT}/${SUBSET}/${PIPELINE}/${PIPELINE}.parquet \
  --acl public-read

# For interpretable version (adjust pipeline name as needed)
INTERPRETABLE_PIPELINE="profiles_var_mad_int"  # Pipeline without final transformations
aws s3 cp outputs/compound/${INTERPRETABLE_PIPELINE}.parquet \
  s3://your-bucket/your-project/profiles/${FORK_OWNER}_jump-profiling-recipe_${YEAR}_${COMMIT}/${SUBSET}/${PIPELINE}/${INTERPRETABLE_PIPELINE}.parquet \
  --acl public-read

# Verify it's accessible
curl -I https://s3.amazonaws.com/your-bucket/your-project/profiles/${FORK_OWNER}_jump-profiling-recipe_${YEAR}_${COMMIT}/${SUBSET}/${PIPELINE}/${PIPELINE}.parquet
```

### 2. Create manifest in your project repo

In your project repository, create the directory structure:

```bash
mkdir -p manifests
```

Create `manifests/profile_index.csv` (replace with your actual URLs from Step 1):

```csv
"subset","url","etag"
"compound","https://s3.amazonaws.com/your-bucket/your-project/profiles/username_jump-profiling-recipe_2024_a1b2c3d/COMPOUND/profiles_var_mad_int_featselect_harmony/profiles_var_mad_int_featselect_harmony.parquet",""
"compound_interpretable","https://s3.amazonaws.com/your-bucket/your-project/profiles/username_jump-profiling-recipe_2024_a1b2c3d/COMPOUND/profiles_var_mad_int_featselect_harmony/profiles_var_mad_int.parquet",""
```

**Note**: Replace `username_jump-profiling-recipe_2024_a1b2c3d` with your actual fork owner, year and commit hash, `COMPOUND` with your data type, and the pipeline strings with your actual processing pipeline.

### 3. Add ETags (for S3 files)

ETags are checksums that ensure data integrity when downloading. Get them from your S3 files:

```bash
# Get ETag for each file (using your variables from Step 1)
curl -I https://s3.amazonaws.com/your-bucket/your-project/profiles/${FORK_OWNER}_jump-profiling-recipe_${YEAR}_${COMMIT}/${SUBSET}/${PIPELINE}/${PIPELINE}.parquet | grep ETag
# Output example: ETag: "d41d8cd98f00b204e9800998ecf8427e-1"
```

Update your CSV with the ETag values (include the quotes). For multiple data types:

```csv
"subset","url","etag"
"compound","https://s3.amazonaws.com/your-bucket/your-project/profiles/username_jump-profiling-recipe_2024_a1b2c3d/COMPOUND/profiles_var_mad_int_featselect_harmony/profiles_var_mad_int_featselect_harmony.parquet","d41d8cd98f00b204e9800998ecf8427e-1"
"compound_interpretable","https://s3.amazonaws.com/your-bucket/your-project/profiles/username_jump-profiling-recipe_2024_a1b2c3d/COMPOUND/profiles_var_mad_int_featselect_harmony/profiles_var_mad_int.parquet","a71b2c3d4e5f6789abcdef1234567890-2"
"orf","https://s3.amazonaws.com/your-bucket/your-project/profiles/username_jump-profiling-recipe_2024_a1b2c3d/ORF/profiles_wellpos_cc_var_mad_outlier_featselect/profiles_wellpos_cc_var_mad_outlier_featselect.parquet","b82c3d4e5f6789abcdef1234567890a7-3"
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

## Tips

- **Multiple versions**: Include both standard and interpretable versions when relevant
- **Document processing**: Add a README explaining your pipeline choices and parameters  
- **Version everything**: Tag your repository when you update profiles or manifests
- **Multiple data types**: You can include ORF, CRISPR, and compound data in the same manifest

## Troubleshooting

**403 Forbidden when accessing S3**: Check that your files have `--acl public-read` permissions

**ETag mismatch**: Re-fetch the ETag after any file updates

**Pipeline not found**: Ensure your pipeline string matches available rules in jump-profiling-recipe

## Example Projects

See these projects for reference:
- [Main JUMP datasets](https://github.com/jump-cellpainting/datasets/blob/main/manifests/profile_index.csv) - the standard pattern
- Your project manifest will follow the same structure

## Need to Process Data First?

See the [jump-profiling-recipe documentation](https://github.com/broadinstitute/jump-profiling-recipe/blob/main/DOCUMENTATION.md) for processing instructions.