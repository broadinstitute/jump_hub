"""Prepare checksum-verified well metadata before running notebook tests."""

import time

import requests

MAX_ATTEMPTS = 3


def download_with_retries(label, download):
    """Retry only download timeouts/connections, never TLS or integrity errors."""
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            path = download()
        except (requests.Timeout, requests.ConnectionError) as error:
            if isinstance(error, requests.exceptions.SSLError) or attempt == MAX_ATTEMPTS:
                raise
            delay = 5 * attempt
            print(
                f"{label}: {type(error).__name__} on attempt {attempt}/{MAX_ATTEMPTS}; "
                f"retrying in {delay}s",
                flush=True,
            )
            time.sleep(delay)
        else:
            print(f"{label}: {path}", flush=True)
            return path


def well_metadata():
    from broad_babel.data import get_table

    return get_table("well")


def main():
    # Reuse the library's pinned URL, hash, and Pooch cache filename rather than
    # duplicating them here. Restored files are verified by Pooch on access.
    download_with_retries("Well metadata", well_metadata)


if __name__ == "__main__":
    main()
