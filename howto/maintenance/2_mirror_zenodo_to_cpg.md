# Mirroring Zenodo Datasets to Cell Painting Gallery

The JUMP_rr feature, match, gallery, and significance tables are published to Zenodo with a stable concept DOI. To keep load times responsive (especially for browser-based tools like Datasette Lite and ggsql-wasm), each Zenodo release is mirrored onto the Cell Painting Gallery (CPG) S3 bucket using `tools/mirror_zenodo_to_cpg.sh`.

## What the script does

For every file in the latest version of a Zenodo concept, the script writes the file to two locations on CPG:

```
s3://cellpainting-gallery/cpg0042-chandrasekaran-jump/source_all/workspace/publication_data/jump_rr/
    <record_id>/<file>/content      # immutable per-version copy
    latest/<file>/content           # mutable pointer to the most recent version
```

`<record_id>` is the Zenodo record ID for that specific version (e.g. `19835081`). Each new Zenodo version gets a new record ID and a new `<record_id>/` directory on CPG; the previous one is left untouched. The `latest/` directory is always overwritten with the newest version, so `broad.io/*` short links can target `latest/` once and never need to be updated again.

The trailing `/content` suffix mirrors Zenodo's own download URL structure (`https://zenodo.org/api/records/<id>/files/<file>/content`). Datasette-Lite derives its table name from the URL's last path segment; preserving `content` as the last segment on both backends keeps the [JUMP_rr metadata JSONs](https://github.com/broadinstitute/monorepo/tree/main/libs/jump_rr/metadata) (which key descriptions under `databases.data.tables.content`) valid against the CPG-served parquet.

Zenodo remains the canonical, citable archive. CPG is the storage origin; in practice browser tools fetch through the CloudFront edge cache that sits in front of the JUMP_rr subtree (`d3dw4c1b79pj57.cloudfront.net`, provisioned by [`cellpainting-gallery-infra`](https://github.com/broadinstitute/cellpainting-gallery-infra)'s `JumpRrCdnStack`). The CDN's 1h cache TTL means a daily-cron mirror update to `latest/` is visible to consumers within an hour without any manual cache invalidation. The mirror script itself writes only to S3 — it doesn't need to know about the CDN.

## When to run it

Run the script after a new version of the Zenodo record has been published. It can also be run on a schedule (e.g. daily cron) - if Zenodo has not changed, the script does not re-upload anything.

## Requirements

- AWS CLI configured with a profile that has write access to the `cellpainting-gallery` bucket. By default the script uses a profile named `cpg`. See the [Cell Painting Gallery contribution guidelines](https://broadinstitute.github.io/cellpainting-gallery/contributing_to_cpg.html).
- `curl` and `jq` on `PATH`.

## Usage

```bash
# Mirror the default Zenodo concept (10408587 - JUMP_rr processed datasets)
./tools/mirror_zenodo_to_cpg.sh

# Preview without uploading
DRY_RUN=1 ./tools/mirror_zenodo_to_cpg.sh

# Mirror a single file (useful for testing)
ONLY_FILE=crispr_gallery.parquet ./tools/mirror_zenodo_to_cpg.sh

# Mirror a different Zenodo concept
CONCEPT_ID=12345678 ./tools/mirror_zenodo_to_cpg.sh

# Use a different AWS profile
AWS_PROFILE_NAME=my-profile ./tools/mirror_zenodo_to_cpg.sh
```

## Credential paths

There are two ways the script can be run, with different credential mechanics:

1. **Direct S3 access (local maintainer use).** A profile like `cpg` mapped to an IAM user that has direct `s3:PutObject` / `s3:GetObject` on the bucket. The script's defaults (`AWS_PROFILE_NAME=cpg`) work as-is. This is the path most contributors will already have via the [Cell Painting Gallery contribution guidelines](https://broadinstitute.github.io/cellpainting-gallery/contributing_to_cpg.html).

2. **S3 Access Grants (CI / infra-issued credentials).** The IAM keys that [`cellpainting-gallery-infra`](https://github.com/broadinstitute/cellpainting-gallery-infra) provisions for a prefix carry only `s3:GetDataAccess`, not direct S3 actions. To use them you must first mint temporary, prefix-scoped credentials and export them as standard AWS env vars:

   ```bash
   creds=$(aws s3control get-data-access \
     --account-id 309624411020 \
     --target "s3://cellpainting-gallery/cpg0042-chandrasekaran-jump/source_all/workspace/publication_data/jump_rr/*" \
     --permission READWRITE --duration-seconds 43200 --region us-east-1 --output json)
   export AWS_ACCESS_KEY_ID=$(jq -r .Credentials.AccessKeyId    <<< "$creds")
   export AWS_SECRET_ACCESS_KEY=$(jq -r .Credentials.SecretAccessKey <<< "$creds")
   export AWS_SESSION_TOKEN=$(jq -r .Credentials.SessionToken   <<< "$creds")
   AWS_PROFILE_NAME="" ./tools/mirror_zenodo_to_cpg.sh
   ```

   The temp credentials live for up to 12 hours, comfortably more than the worst-case mirror runtime. The GitHub Actions workflow (`.github/workflows/mirror_zenodo.yml`) does exactly this in a dedicated step before invoking the script, so the script itself stays Access-Grants-unaware.

## How idempotency works

The script stores the Zenodo MD5 checksum as S3 user metadata on each uploaded object under the key `zenodo-md5`. On subsequent runs, the script checks the existing object's `zenodo-md5` against the Zenodo file's MD5:

- Match: skip the upload. The version copy is already correct.
- No match (or object missing): stream the file from Zenodo to S3.

The `latest/` copy is always refreshed via a server-side S3-to-S3 copy from the version directory. This is cheap and ensures `latest/` self-heals if it ever drifts.

## Streaming behavior

The script pipes `curl` directly into `aws s3 cp -`, so the file is never written to local disk. This matters for the larger files in the JUMP_rr record (the compound cosine-similarity table is around 49 GB), which would not fit on a typical CI runner's local disk.

## Why a `latest/` directory and not symlinks

S3 has no native symlink mechanism. The two-directory pattern (immutable `<record_id>/` plus mutable `latest/`) is the conventional workaround: callers can either pin to a specific version for reproducibility or follow `latest/` for the current data. Updates to `latest/` are atomic at the file level.

## What's not covered by this script

- Publishing to Zenodo. The Zenodo release is cut by whoever owns the JUMP_rr generation pipeline. This script only mirrors what is already on Zenodo.
- Updating `broad.io/*` short links. If `latest/` is the persistent target, no updates are needed for ongoing releases. If a short link still references a Zenodo URL, that's a one-time repointing that lives outside this script.
- Other artifacts on CPG (such as the v0.13 metadata DuckDB at `publication_data/datasets/v0.13/`) that are not sourced from this Zenodo concept.
