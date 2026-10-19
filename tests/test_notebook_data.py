"""Offline regression tests for notebook data preparation."""

import hashlib
import importlib.util
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock

import pooch
import pytest
import requests

SPEC = importlib.util.spec_from_file_location(
    "prepare_notebook_data",
    Path(__file__).resolve().parents[1] / "tools" / "prepare_notebook_data.py",
)
prepare = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(prepare)


@pytest.fixture(autouse=True)
def no_network(monkeypatch):
    def reject_request(*args, **kwargs):
        raise AssertionError("Unit tests must not access the network")

    monkeypatch.setattr(requests.Session, "request", reject_request)


@pytest.fixture
def delays(monkeypatch):
    recorded = []
    monkeypatch.setattr(prepare, "time", SimpleNamespace(sleep=recorded.append))
    return recorded


@pytest.mark.parametrize(
    "error", [requests.ReadTimeout, requests.ConnectTimeout, requests.ConnectionError]
)
def test_transient_download_retries(error, delays):
    download = Mock(side_effect=[error("temporary"), error("temporary"), "verified-file"])
    assert prepare.download_with_retries("metadata", download) == "verified-file"
    assert download.call_count == 3
    assert delays == [5, 10]


def test_persistent_timeout_fails(delays):
    download = Mock(side_effect=requests.ReadTimeout("still unavailable"))
    with pytest.raises(requests.ReadTimeout, match="still unavailable"):
        prepare.download_with_retries("metadata", download)
    assert download.call_count == 3
    assert delays == [5, 10]


@pytest.mark.parametrize(
    "error",
    [
        requests.exceptions.SSLError("certificate verification failed"),
        requests.HTTPError("404 Not Found"),
        ValueError("checksum mismatch"),
        RuntimeError("code defect"),
    ],
)
def test_other_errors_are_not_retried(error, delays):
    download = Mock(side_effect=error)
    with pytest.raises(type(error)):
        prepare.download_with_retries("metadata", download)
    assert download.call_count == 1
    assert delays == []


def test_cache_is_verified_and_reused(tmp_path, delays):
    payload = b"verified metadata\n"
    calls = []

    def downloader(url, output_file, pooch_instance):
        calls.append(url)
        Path(output_file).write_bytes(b"partial" if len(calls) == 1 else payload)
        if len(calls) == 1:
            raise requests.ReadTimeout("interrupted download")

    def fetch():
        return pooch.retrieve(
            "https://example.invalid/metadata.csv",
            known_hash=hashlib.sha256(payload).hexdigest(),
            fname="metadata.csv",
            path=tmp_path,
            downloader=downloader,
        )

    cached = Path(prepare.download_with_retries("metadata", fetch))
    assert cached.read_bytes() == payload
    assert len(calls) == 2
    assert delays == [5]
    assert prepare.download_with_retries("metadata", fetch) == str(cached)
    assert len(calls) == 2  # Warm cache: no download.

    cached.write_bytes(b"corrupt cache")
    prepare.download_with_retries("metadata", fetch)
    assert cached.read_bytes() == payload  # Restored caches are not blindly trusted.
    assert len(calls) == 3


def test_bad_download_is_not_cached_or_retried(tmp_path, delays):
    calls = []

    def downloader(url, output_file, pooch_instance):
        calls.append(url)
        Path(output_file).write_bytes(b"wrong contents")

    def fetch():
        return pooch.retrieve(
            "https://example.invalid/metadata.csv",
            known_hash=hashlib.sha256(b"expected contents").hexdigest(),
            fname="metadata.csv",
            path=tmp_path,
            downloader=downloader,
        )

    with pytest.raises(ValueError):
        prepare.download_with_retries("metadata", fetch)
    assert len(calls) == 1
    assert delays == []
    assert not (tmp_path / "metadata.csv").exists()


def test_main_prepares_well_metadata(monkeypatch, delays):
    well = Mock(return_value="verified-well.csv.gz")
    monkeypatch.setattr(prepare, "well_metadata", well)
    prepare.main()
    well.assert_called_once_with()
    assert delays == []
