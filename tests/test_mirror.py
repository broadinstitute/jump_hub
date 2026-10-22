"""Offline tests: no AWS credentials, network, or real object mutations."""
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("verified_stream", ROOT / "tools/upload_verified_stream.py")
stream = importlib.util.module_from_spec(spec)
spec.loader.exec_module(stream)


class Response(io.BytesIO):
    def __init__(self, data, length=None, interrupt=False):
        super().__init__(data)
        self.headers = {} if length is None else {"Content-Length": str(length)}
        self.interrupt = interrupt

    def read(self, count=-1):
        if self.interrupt and self.tell():
            raise OSError("Download interrupted")
        return super().read(count)


class FakeS3:
    def __init__(self, size, md5, fail=None):
        self.size, self.md5, self.fail = size, md5, fail
        self.calls, self.parts = [], {}
        self.visible = b"pre-existing valid object"

    def __call__(self, operation, args, profile):
        self.calls.append(operation)
        if operation == self.fail:
            raise RuntimeError("Simulated S3 failure")
        if operation == "create-multipart-upload":
            self.metadata = json.loads(args[args.index("--metadata") + 1])
            return {"UploadId": "test-upload"}
        if operation == "upload-part":
            number = int(args[args.index("--part-number") + 1])
            self.parts[number] = Path(args[args.index("--body") + 1]).read_bytes()
            return {"ETag": f'"part-{number}"'}
        if operation == "complete-multipart-upload":
            path = args[args.index("--multipart-upload") + 1].removeprefix("file://")
            parts = json.loads(Path(path).read_text())["Parts"]
            assert [p["PartNumber"] for p in parts] == list(range(1, len(parts) + 1))
            self.visible = b"".join(self.parts[p["PartNumber"]] for p in parts)
            return {"ETag": '"complete"'}
        if operation == "head-object":
            return {"ContentLength": len(self.visible), "Metadata": self.metadata}
        if operation == "abort-multipart-upload":
            self.parts.clear()
            return {}
        raise AssertionError(operation)


class StreamTests(unittest.TestCase):
    data = b"verified parquet bytes for a fake multipart upload"

    def run_upload(self, body=None, size=None, md5=None, length=None, interrupt=False, fail=None):
        body = self.data if body is None else body
        size = len(self.data) if size is None else size
        md5 = hashlib.md5(self.data).hexdigest() if md5 is None else md5
        self.s3 = FakeS3(size, md5, fail=fail)
        return stream.upload_verified("https://example.invalid/file", "bucket", "version/file/content", size, md5, "123",
                                      opener=lambda *a, **kw: Response(body, length, interrupt), runner=self.s3, part_size=8)

    def test_verified_bytes_commit_atomically(self):
        result = self.run_upload(length=len(self.data))
        self.assertEqual(self.s3.visible, self.data)
        self.assertEqual(result["size"], len(self.data))
        self.assertEqual(self.s3.metadata["zenodo-md5"], hashlib.md5(self.data).hexdigest())
        self.assertEqual(self.s3.metadata["zenodo-record-id"], "123")
        self.assertNotIn("abort-multipart-upload", self.s3.calls)

    def test_truncated_body_never_commits(self):
        with self.assertRaises(ValueError):
            self.run_upload(body=self.data[:-3])
        self.assertNotIn("complete-multipart-upload", self.s3.calls)
        self.assertIn("abort-multipart-upload", self.s3.calls)
        self.assertEqual(self.s3.visible, b"pre-existing valid object")

    def test_wrong_same_length_content_never_commits(self):
        with self.assertRaises(ValueError):
            self.run_upload(body=b"X" + self.data[1:])
        self.assertNotIn("complete-multipart-upload", self.s3.calls)
        self.assertIn("abort-multipart-upload", self.s3.calls)

    def test_too_long_content_never_commits(self):
        with self.assertRaises(ValueError):
            self.run_upload(body=self.data + b"extra")
        self.assertNotIn("complete-multipart-upload", self.s3.calls)
        self.assertIn("abort-multipart-upload", self.s3.calls)

    def test_wrong_header_stops_before_s3_mutation(self):
        with self.assertRaises(ValueError):
            self.run_upload(length=len(self.data) - 1)
        self.assertEqual(self.s3.calls, [])

    def test_interrupted_download_aborts(self):
        with self.assertRaises(OSError):
            self.run_upload(interrupt=True)
        self.assertNotIn("complete-multipart-upload", self.s3.calls)
        self.assertIn("abort-multipart-upload", self.s3.calls)

    def test_part_upload_failure_aborts(self):
        with self.assertRaises(RuntimeError):
            self.run_upload(fail="upload-part")
        self.assertNotIn("complete-multipart-upload", self.s3.calls)
        self.assertIn("abort-multipart-upload", self.s3.calls)

    def test_completion_failure_attempts_abort(self):
        with self.assertRaises(RuntimeError):
            self.run_upload(fail="complete-multipart-upload")
        self.assertIn("abort-multipart-upload", self.s3.calls)
        self.assertEqual(self.s3.visible, b"pre-existing valid object")


@unittest.skipUnless(shutil.which("jq"), "jq is required by the mirror script")
class CacheTests(unittest.TestCase):
    def mirror(self, stored_size, stored_md5):
        md5 = "a" * 32
        record = {"id": 123, "doi": "test", "metadata": {"publication_date": "2026-10-22"},
                  "files": [{"key": "table.parquet", "size": 20, "checksum": "md5:" + md5,
                             "links": {"self": "https://example.invalid/file"}}]}
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            for name, content in {
                "curl": "import os; print(os.environ['MOCK_RECORD'])",
                "aws": "import os,sys; assert sys.argv[1:3]==['s3api','head-object']; print(os.environ['MOCK_HEAD'])",
            }.items():
                executable = folder / name
                executable.write_text("#!/usr/bin/env python3\n" + content + "\n")
                executable.chmod(0o755)
            env = dict(os.environ, PATH=str(folder) + os.pathsep + os.environ["PATH"],
                       DRY_RUN="1", AWS_PROFILE_NAME="", ONLY_FILE="", MOCK_RECORD=json.dumps(record),
                       MOCK_HEAD=json.dumps({"ContentLength": stored_size, "Metadata": {"zenodo-md5": stored_md5}}))
            return subprocess.check_output(["bash", str(ROOT / "tools/mirror_zenodo_to_cpg.sh")], env=env, text=True)

    def test_valid_cached_file_is_skipped(self):
        output = self.mirror(20, "a" * 32)
        self.assertIn("skip upload:", output)
        self.assertNotIn("upload_verified_stream.py", output)

    def test_truncated_cached_file_with_expected_metadata_is_not_skipped(self):
        output = self.mirror(12, "a" * 32)
        self.assertNotIn("skip upload:", output)
        self.assertIn("upload_verified_stream.py", output)

    def test_wrong_checksum_is_not_skipped(self):
        output = self.mirror(20, "b" * 32)
        self.assertNotIn("skip upload:", output)
        self.assertIn("upload_verified_stream.py", output)


if __name__ == "__main__":
    unittest.main()
