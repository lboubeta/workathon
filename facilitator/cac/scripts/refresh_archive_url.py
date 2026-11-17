#!/usr/bin/env python3
"""Upload facilitator-starter.tar.gz to S3 and print a 7-daypresigned GET URL.

Usage:
  python3 refresh_archive_url.py
  export FACILITATOR_STARTER_URL=$(python3 refresh_archive_url.py)
"""

from __future__ import annotations

import argparse
import pathlib
import sys

import boto3

DEFAULT_BUCKET = "bankinter-workathon-facilitator-938412772717"
DEFAULT_KEY = "facilitator-starter.tar.gz"
DEFAULT_REGION = "eu-west-1"
ARCHIVE = pathlib.Path(__file__).resolve().parents[1] / "files" / "facilitator-starter.tar.gz"


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--bucket", default=DEFAULT_BUCKET)
    p.add_argument("--key", default=DEFAULT_KEY)
    p.add_argument("--region", default=DEFAULT_REGION)
    p.add_argument("--expires", type=int, default=604800)
    p.add_argument("--skip-upload", action="store_true")
    args = p.parse_args()

    if not ARCHIVE.exists():
        print(f"Missing archive: {ARCHIVE}", file=sys.stderr)
        return 1

    s3 = boto3.client("s3", region_name=args.region)
    if not args.skip_upload:
        s3.upload_file(str(ARCHIVE), args.bucket, args.key)

    # Prefer a clean public URL (no query string). AAP archive SCM breaks on
    # quoted/presigned URLs with ?Signature=...
    public = f"https://{args.bucket}.s3.{args.region}.amazonaws.com/{args.key}"
    try:
        import urllib.request

        with urllib.request.urlopen(public, timeout=10) as resp:
            if 200 <= resp.status < 300:
                print(public)
                return 0
    except Exception:
        pass

    url = s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": args.bucket, "Key": args.key},
        ExpiresIn=args.expires,
    )
    print(url)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
