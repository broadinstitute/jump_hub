#!/usr/bin/env bash
# Mirror a Zenodo record onto the Cell Painting Gallery S3 bucket.
#
# Streams each file from Zenodo straight to S3 (no large local downloads),
# writing to two paths per file:
#   - <S3_PREFIX>/<record_id>/<file>/content   immutable per-version copy
#   - <S3_PREFIX>/latest/<file>/content        mutable pointer to the most recent
#
# The trailing /content suffix mirrors Zenodo's own download URL structure
# (https://zenodo.org/api/records/<id>/files/<file>/content) so that
# Datasette-Lite, which derives its table name from the URL's last path
# segment, registers the parquet under the same name on both backends. This
# lets broad.io/* short links be repointed by swapping only the parquet=
# URL parameter -- metadata table keys (`databases.data.tables.content` in
# the jump_rr metadata JSONs) remain valid.
#
# Idempotent: stores the Zenodo MD5 as S3 user metadata `zenodo-md5` and skips
# uploads when the existing object already carries the same checksum.
#
# Usage:
#   ./mirror_zenodo_to_cpg.sh                  # mirror default record
#   DRY_RUN=1 ./mirror_zenodo_to_cpg.sh        # print actions without uploading
#   CONCEPT_ID=10408587 ./mirror_zenodo_to_cpg.sh
#   ONLY_FILE=crispr_gallery.parquet ./mirror_zenodo_to_cpg.sh

set -euo pipefail

CONCEPT_ID="${CONCEPT_ID:-10408587}"
S3_BUCKET="${S3_BUCKET:-cellpainting-gallery}"
S3_PREFIX="${S3_PREFIX:-cpg0042-chandrasekaran-jump/source_all/workspace/publication_data/jump_rr}"
AWS_PROFILE_NAME="${AWS_PROFILE_NAME-cpg}"
DRY_RUN="${DRY_RUN:-0}"
ONLY_FILE="${ONLY_FILE:-}"

# Build the optional `--profile <name>` arg only when AWS_PROFILE_NAME is set
# and non-empty. In GitHub Actions, aws-actions/configure-aws-credentials
# exports credentials as environment variables and does not create a
# `default` profile, so passing `--profile default` would fail.
profile_args=()
if [ -n "${AWS_PROFILE_NAME}" ]; then
    profile_args=(--profile "$AWS_PROFILE_NAME")
fi

log() { printf '%s %s\n' "[$(date -u +%H:%M:%SZ)]" "$*"; }

run_aws() {
    if [ "$DRY_RUN" = "1" ]; then
        printf '  DRY-RUN: aws %s\n' "$*"
    else
        aws "$@"
    fi
}

log "Resolving latest version of Zenodo concept $CONCEPT_ID"
record_json=$(curl -fsSL "https://zenodo.org/api/records/${CONCEPT_ID}/versions/latest")
record_id=$(printf '%s' "$record_json" | jq -r '.id')
record_doi=$(printf '%s' "$record_json" | jq -r '.doi')
pub_date=$(printf '%s' "$record_json" | jq -r '.metadata.publication_date')
file_count=$(printf '%s' "$record_json" | jq '.files | length')

log "Latest record: $record_id (doi $record_doi, published $pub_date, $file_count files)"
log "Target prefix: s3://${S3_BUCKET}/${S3_PREFIX}/{${record_id},latest}/"

skipped=0
uploaded=0
synced=0

while IFS=$'\t' read -r name url size md5; do
    if [ -n "$ONLY_FILE" ] && [ "$name" != "$ONLY_FILE" ]; then
        continue
    fi

    version_key="${S3_PREFIX}/${record_id}/${name}/content"
    latest_key="${S3_PREFIX}/latest/${name}/content"
    version_uri="s3://${S3_BUCKET}/${version_key}"
    latest_uri="s3://${S3_BUCKET}/${latest_key}"

    log "FILE $name (size=${size}, md5=${md5})"

    existing_md5=$(aws s3api head-object \
        --bucket "$S3_BUCKET" --key "$version_key" \
        "${profile_args[@]}" 2>/dev/null \
        | jq -r '.Metadata."zenodo-md5" // empty' || true)

    if [ "$existing_md5" = "$md5" ]; then
        log "  skip upload: $version_uri already has matching zenodo-md5"
        skipped=$((skipped + 1))
    else
        log "  upload: streaming Zenodo -> $version_uri"
        if [ "$DRY_RUN" = "1" ]; then
            printf '  DRY-RUN: curl -fsSL %s | aws s3 cp - %s --expected-size %s --metadata zenodo-md5=%s,zenodo-record-id=%s %s\n' \
                "$url" "$version_uri" "$size" "$md5" "$record_id" "${profile_args[*]}"
        else
            curl -fsSL "$url" \
                | aws s3 cp - "$version_uri" \
                    --expected-size "$size" \
                    --metadata "zenodo-md5=${md5},zenodo-record-id=${record_id}" \
                    "${profile_args[@]}"
        fi
        uploaded=$((uploaded + 1))
    fi

    log "  sync: $version_uri -> $latest_uri"
    run_aws s3 cp "$version_uri" "$latest_uri" \
        --metadata-directive REPLACE \
        --metadata "zenodo-md5=${md5},zenodo-record-id=${record_id}" \
        "${profile_args[@]}" \
        --only-show-errors
    synced=$((synced + 1))
done < <(printf '%s' "$record_json" \
    | jq -r '.files[] | [.key, .links.self, (.size|tostring), (.checksum|sub("^md5:"; ""))] | @tsv')

log "Done. uploaded=$uploaded skipped=$skipped synced=$synced"
