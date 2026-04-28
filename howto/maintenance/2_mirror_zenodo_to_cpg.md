# Mirroring Zenodo Datasets to Cell Painting Gallery

The JUMP_rr feature, match, gallery, and significance tables are published to Zenodo with a stable concept DOI. To keep load times responsive (especially for browser-based tools like Datasette Lite and ggsql-wasm), each Zenodo release is mirrored onto the Cell Painting Gallery (CPG) S3 bucket using `tools/mirror_zenodo_to_cpg.sh`.

## What the script does

For every file in the latest version of a Zenodo concept, the script writes the file to two locations on CPG:

```
s3://cellpainting-gallery/cpg0042-chandrasekaran-jump/source_all/workspace/publication_data/jump_rr/
    <record_id>/<file>      # immutable per-version copy
    latest/<file>           # mutable pointer to the most recent version
```

`<record_id>` is the Zenodo record ID for that specific version (e.g. `19835081`). Each new Zenodo version gets a new record ID and a new `<record_id>/` directory on CPG; the previous one is left untouched. The `latest/` directory is always overwritten with the newest version, so `broad.io/*` short links can target `latest/` once and never need to be updated again.

Zenodo remains the canonical, citable archive. CPG is the runtime origin that browser tools fetch from.

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
