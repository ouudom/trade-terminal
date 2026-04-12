"""
POST bias snapshots from bias_staging.json to the Trade Terminal API.
Idempotent — the endpoint upserts on (instrument_id, timeframe, valid_from).

Usage (from anywhere with Python 3):
    python scripts/insert_bias.py [path/to/bias_staging.json] [--api-url URL]

Defaults:
    JSON path : ~/trading/output/bias_staging.json
    API URL   : http://localhost:8000
"""
import sys
import json
import argparse
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

DEFAULT_STAGING_PATH = Path.home() / "trading" / "output" / "bias_staging.json"
DEFAULT_API_URL = "http://localhost:8000"
ENDPOINT = "/bias/insert-bias"


def post_bias(staging_path: Path, api_url: str) -> None:
    if not staging_path.exists():
        print(f"ERROR: Staging file not found: {staging_path}", file=sys.stderr)
        sys.exit(1)

    with open(staging_path, "r") as f:
        records = json.load(f)

    print(f"Loaded {len(records)} records from {staging_path}")
    print(f"POSTing to {api_url}{ENDPOINT} ...\n")

    body = json.dumps(records).encode("utf-8")
    req = Request(
        url=f"{api_url}{ENDPOINT}",
        data=body,
        method="POST",
        headers={"Content-Type": "application/json"},
    )

    try:
        with urlopen(req, timeout=15) as resp:
            response = json.loads(resp.read().decode("utf-8"))
    except HTTPError as e:
        error_body = e.read().decode("utf-8")
        print(f"ERROR {e.code}: {error_body}", file=sys.stderr)
        sys.exit(1)
    except URLError as e:
        print(f"ERROR: Could not reach API at {api_url} — is the backend running?", file=sys.stderr)
        print(f"  Detail: {e.reason}", file=sys.stderr)
        sys.exit(1)

    inserted = response.get("inserted", 0)
    results = response.get("results", [])

    for r in results:
        print(f"  [{r['action'].upper()}] instrument_id={r['instrument_id']} -> snapshot_id={r['snapshot_id']}")

    print(f"\nDone: {inserted} bias snapshots upserted.")


def main():
    parser = argparse.ArgumentParser(description="Insert bias staging JSON via API")
    parser.add_argument(
        "staging_path",
        nargs="?",
        type=Path,
        default=DEFAULT_STAGING_PATH,
        help=f"Path to bias_staging.json (default: {DEFAULT_STAGING_PATH})",
    )
    parser.add_argument(
        "--api-url",
        default=DEFAULT_API_URL,
        help=f"Base URL of the Trade Terminal API (default: {DEFAULT_API_URL})",
    )
    args = parser.parse_args()
    post_bias(args.staging_path, args.api_url)


if __name__ == "__main__":
    main()
