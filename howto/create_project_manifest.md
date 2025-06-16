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

Make your profiles publicly accessible:

```bash
# Upload to S3 (replace with your bucket and path)
aws s3 cp outputs/compound/profiles_var_mad_int_featselect_harmony.parquet \
  s3://your-bucket/your-project/profiles/ --acl public-read

# Verify it's accessible
curl -I https://s3.amazonaws.com/your-bucket/your-project/profiles/profiles_var_mad_int_featselect_harmony.parquet
```

### 2. Create manifest in your project repo

In your project repository, create the directory structure:

```bash
mkdir -p manifests
```

Create `manifests/profile_index.csv`:

```csv
"subset","url","etag"
"compound","https://s3.amazonaws.com/your-bucket/your-project/profiles/profiles_var_mad_int_featselect_harmony.parquet",""
"compound_interpretable","https://s3.amazonaws.com/your-bucket/your-project/profiles/profiles_var_mad_outlier.parquet",""
```

### 3. Add ETags (for S3 files)

ETags ensure data integrity. Get them from your S3 files:

```bash
# Get ETag for each file
curl -I https://s3.amazonaws.com/your-bucket/your-project/profiles/profiles_var_mad_int_featselect_harmony.parquet | grep ETag
# Output example: ETag: "d41d8cd98f00b204e9800998ecf8427e-1"
```

Update your CSV with the ETag values (include the quotes):

```csv
"subset","url","etag"
"compound","https://s3.amazonaws.com/your-bucket/your-project/profiles/profiles_var_mad_int_featselect_harmony.parquet","d41d8cd98f00b204e9800998ecf8427e-1"
"compound_interpretable","https://s3.amazonaws.com/your-bucket/your-project/profiles/profiles_var_mad_outlier.parquet","a71b2c3d4e5f6789abcdef1234567890-2"
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

## Tips

- **Multiple versions**: Include both standard and interpretable versions when relevant
- **Documentation**: Add a README to your manifests/ folder explaining your processing choices
- **Versioning**: Tag your repository when you update the manifest

## Example Projects

See these projects for reference:
- [Main JUMP datasets](https://github.com/jump-cellpainting/datasets/blob/main/manifests/profile_index.csv) - the standard pattern
- Your project manifest will follow the same structure

## Need to Process Data First?

See the [jump-profiling-recipe documentation](https://github.com/broadinstitute/jump-profiling-recipe/blob/main/DOCUMENTATION.md) for processing instructions.