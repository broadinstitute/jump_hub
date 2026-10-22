#!/usr/bin/env python3
"""Mirror a public download to S3, completing the object only after MD5/size checks.

Uses the existing AWS CLI credentials/profile and at most one 64 MiB temporary
part on disk. Failed transfers are aborted; they cannot leave a truncated object
carrying the expected Zenodo checksum or overwrite an existing valid object.
"""

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
from urllib.request import urlopen

PART_SIZE = 64 * 1024 * 1024


def aws_json(operation, arguments, profile):
    command = ["aws", "s3api", operation, *arguments, "--output", "json"]
    if profile:
        command.extend(["--profile", profile])
    result = subprocess.run(command, check=True, stdout=subprocess.PIPE, text=True)
    return json.loads(result.stdout) if result.stdout.strip() else {}


def upload_verified(url, bucket, key, size, md5, record_id, profile="", *,
                    opener=urlopen, runner=aws_json, part_size=PART_SIZE):
    if not url.startswith("https://") or size <= 0 or not re.fullmatch(r"[0-9a-f]{32}", md5):
        raise ValueError("Expected HTTPS URL, positive size and lowercase MD5")
    if part_size <= 0 or (size + part_size - 1) // part_size > 10000:
        raise ValueError("Invalid S3 multipart size/count")
    metadata = {"zenodo-md5": md5, "zenodo-record-id": str(record_id)}
    target = ["--bucket", bucket, "--key", key]
    upload_id = None
    completed = False
    try:
        with opener(url, timeout=120) as source, tempfile.TemporaryDirectory(prefix="jump-rr-mirror-") as folder:
            length = source.headers.get("Content-Length")
            if length is not None and int(length) != size:
                raise ValueError(f"Unexpected Content-Length: {length}, expected {size}")
            created = runner("create-multipart-upload", [*target, "--metadata", json.dumps(metadata)], profile)
            upload_id = created["UploadId"]
            part_path = Path(folder) / "part"
            parts, total, digest = [], 0, hashlib.md5()
            while True:
                chunk = source.read(part_size)
                if not chunk:
                    break
                total += len(chunk)
                if total > size:
                    raise ValueError("Source is longer than the published size")
                digest.update(chunk)
                part_path.write_bytes(chunk)
                part_number = len(parts) + 1
                response = runner("upload-part", [*target, "--upload-id", upload_id,
                                  "--part-number", str(part_number), "--body", str(part_path)], profile)
                parts.append({"PartNumber": part_number, "ETag": response["ETag"]})
                if part_number == 1 or part_number % 16 == 0:
                    print(f"  staged {total}/{size} bytes ({part_number} parts)", flush=True)
            if total != size or digest.hexdigest() != md5:
                raise ValueError(f"Downloaded content failed size/MD5 verification ({total}/{size} bytes)")
            # S3 does not expose/replace the final object until this succeeds.
            manifest = Path(folder) / "parts.json"
            manifest.write_text(json.dumps({"Parts": parts}))
            runner("complete-multipart-upload", [*target, "--upload-id", upload_id,
                   "--multipart-upload", f"file://{manifest}"], profile)
            completed = True
        head = runner("head-object", target, profile)
        if (head["ContentLength"] != size or head.get("Metadata", {}).get("zenodo-md5") != md5
                or head.get("Metadata", {}).get("zenodo-record-id") != str(record_id)):
            raise ValueError("Stored S3 object does not match the verified transfer")
        return {"size": total, "md5": md5, "parts": len(parts)}
    finally:
        if upload_id is not None and not completed:
            try:
                runner("abort-multipart-upload", [*target, "--upload-id", upload_id], profile)
            except Exception:
                # A timed-out completion may already have committed a verified
                # object; abort then returns NoSuchUpload. Preserve original error.
                print("Warning: multipart abort failed; inspect S3 upload state.", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url")
    parser.add_argument("bucket")
    parser.add_argument("key")
    parser.add_argument("size", type=int)
    parser.add_argument("md5")
    parser.add_argument("record_id")
    parser.add_argument("--profile", default="")
    args = parser.parse_args()
    print(json.dumps(upload_verified(**vars(args))))


if __name__ == "__main__":
    main()
