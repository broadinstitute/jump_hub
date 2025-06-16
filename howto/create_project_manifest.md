# Creating a Project Manifest

Have custom-processed JUMP profiles? Here's how to share them with others.

## Prerequisites

- Processed profiles from [jump-profiling-recipe](https://github.com/broadinstitute/jump-profiling-recipe/blob/main/DOCUMENTATION.md)
- AWS CLI configured (for S3 upload)
- A GitHub repository for your project

## Starting Point

You've already processed your profiles and they're in:
```
outputs/{scenario}/{pipeline}.parquet
```

Now let's make them accessible to others.

## Steps

### 1. Upload to S3

Make your profiles publicly accessible using a structured path that includes processing provenance:

```bash
# Get the commit hash from your jump-profiling-recipe
cd /path/to/jump-profiling-recipe
COMMIT=$(git rev-parse --short HEAD)
echo "Using commit: $COMMIT"

# Upload with structured path including commit info
aws s3 cp outputs/compound/profiles_var_mad_int_featselect_harmony.parquet \
  s3://your-bucket/your-project/profiles/jump-profiling-recipe_2024_${COMMIT}/COMPOUND/profiles_var_mad_int_featselect_harmony/profiles_var_mad_int_featselect_harmony.parquet \
  --acl public-read

# For interpretable version
aws s3 cp outputs/compound/profiles_var_mad_int.parquet \
  s3://your-bucket/your-project/profiles/jump-profiling-recipe_2024_${COMMIT}/COMPOUND/profiles_var_mad_int_featselect_harmony/profiles_var_mad_int.parquet \
  --acl public-read

# Verify it's accessible
curl -I https://s3.amazonaws.com/your-bucket/your-project/profiles/jump-profiling-recipe_2024_${COMMIT}/COMPOUND/profiles_var_mad_int_featselect_harmony/profiles_var_mad_int_featselect_harmony.parquet
```

### 2. Create manifest in your project repo

In your project repository, create the directory structure:

```bash
mkdir -p manifests
```

Create `manifests/profile_index.csv`:

```csv
"subset","url","etag"
"compound","https://s3.amazonaws.com/your-bucket/your-project/profiles/jump-profiling-recipe_2024_a1b2c3d/COMPOUND/profiles_var_mad_int_featselect_harmony/profiles_var_mad_int_featselect_harmony.parquet",""
"compound_interpretable","https://s3.amazonaws.com/your-bucket/your-project/profiles/jump-profiling-recipe_2024_a1b2c3d/COMPOUND/profiles_var_mad_int_featselect_harmony/profiles_var_mad_int.parquet",""
```

### 3. Add ETags (for S3 files)

ETags ensure data integrity. Get them from your S3 files:

```bash
# Get ETag for each file
curl -I https://s3.amazonaws.com/your-bucket/your-project/profiles/jump-profiling-recipe_2024_a1b2c3d/COMPOUND/profiles_var_mad_int_featselect_harmony/profiles_var_mad_int_featselect_harmony.parquet | grep ETag
# Output example: ETag: "d41d8cd98f00b204e9800998ecf8427e-1"
```

Update your CSV with the ETag values (include the quotes):

```csv
"subset","url","etag"
"compound","https://s3.amazonaws.com/your-bucket/your-project/profiles/jump-profiling-recipe_2024_a1b2c3d/COMPOUND/profiles_var_mad_int_featselect_harmony/profiles_var_mad_int_featselect_harmony.parquet","d41d8cd98f00b204e9800998ecf8427e-1"
"compound_interpretable","https://s3.amazonaws.com/your-bucket/your-project/profiles/jump-profiling-recipe_2024_a1b2c3d/COMPOUND/profiles_var_mad_int_featselect_harmony/profiles_var_mad_int.parquet","a71b2c3d4e5f6789abcdef1234567890-2"
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

## Understanding Your Files

Your processed profiles follow this naming pattern:
```
profiles_{pipeline_steps}.parquet
```

For example:
- `profiles_var_mad_int_featselect_harmony.parquet` - fully processed with batch correction
- `profiles_var_mad_outlier.parquet` - interpretable version without transformations

Include both versions in your manifest when relevant.

## Making Your Processing Traceable

Your manifest URLs should follow the same structure as the main JUMP datasets to ensure full reproducibility. This allows others to trace back exactly how your profiles were generated.

### URL Structure Pattern

Following the [JUMP dataset convention](../scripts/11_retrieve_profiles.py), your URLs should encode:

```
https://s3.amazonaws.com/bucket/project/profiles/jump-profiling-recipe_YEAR_COMMIT/SUBSET/pipeline_directory/filename.parquet
```

**Components:**
- `jump-profiling-recipe_2024_a1b2c3d` - Tool name, year, and commit hash
- `SUBSET/` - Data type (COMPOUND, ORF, CRISPR, etc.)
- `pipeline_directory/` - The exact pipeline string used
- `filename.parquet` - Final output file

### How Others Can Reproduce Your Processing

With this URL structure, anyone can:

1. **Extract the commit**: `jump-profiling-recipe_2024_a1b2c3d` → commit `a1b2c3d`
2. **Extract the pipeline**: `profiles_var_mad_int_featselect_harmony` 
3. **Find the config**: Check `inputs/config/` in jump-profiling-recipe at that commit
4. **Match the pipeline**: Find the config file where `"pipeline"` matches your string

### Save Your Configuration

Along with your manifest, save the exact configuration used:

```bash
# In your project repo
mkdir -p processing_configs
cp /path/to/jump-profiling-recipe/inputs/config/your_config.json processing_configs/
git add processing_configs/your_config.json manifests/profile_index.csv
```

This ensures complete reproducibility of your processing pipeline.

## Tips

- **Follow URL conventions**: Use the structured path format with commit information
- **Save your config**: Include the exact jump-profiling-recipe config in your repo
- **Multiple versions**: Include both standard and interpretable versions when relevant
- **Document processing**: Add a README explaining your pipeline choices and parameters
- **Version everything**: Tag your repository when you update profiles or manifests
- **Cross-reference**: Link to the specific commit and config used in your documentation

## Example Projects

See these projects for reference:
- [Main JUMP datasets](https://github.com/jump-cellpainting/datasets/blob/main/manifests/profile_index.csv) - the standard pattern
- Your project manifest will follow the same structure

## Need to Process Data First?

See the [jump-profiling-recipe documentation](https://github.com/broadinstitute/jump-profiling-recipe/blob/main/DOCUMENTATION.md) for processing instructions.