#!/usr/bin/env python3
"""Upload a local data file to a Databricks Unity Catalog Volume.

Important:
    A Databricks Workspace folder is for notebooks and source files. Queryable
    CSV, JSON, and Parquet data should be uploaded to a Unity Catalog Volume.

Required environment variables:
    DATABRICKS_HOST  Example: https://dbc-xxxxxxxx-xxxx.cloud.databricks.com
    DATABRICKS_TOKEN A newly generated Databricks personal access token

Example (Windows PowerShell):
    $env:DATABRICKS_HOST = "https://dbc-xxxxxxxx-xxxx.cloud.databricks.com"
    $env:DATABRICKS_TOKEN = "<NEW_TOKEN>"

    python upload_to_databricks_volume.py `
      --file "C:\\data\\students.csv" `
      --volume-path "/Volumes/main/default/tinitiate_data/bronze/students"

The script creates the destination directory when needed, uploads the file,
and prints PySpark and SQL examples for querying it.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path, PurePosixPath
from urllib.parse import quote

try:
    import requests
except ImportError:  # Gives Windows users a clear installation instruction.
    print(
        "ERROR: The 'requests' package is required. "
        "Install it with: python -m pip install requests",
        file=sys.stderr,
    )
    raise SystemExit(2)


CHUNK_SIZE = 8 * 1024 * 1024
SUPPORTED_EXTENSIONS = {".csv", ".json", ".jsonl", ".parquet"}


class UploadError(RuntimeError):
    """Raised when Databricks rejects an upload operation."""


def normalize_host(host: str) -> str:
    host = host.strip().rstrip("/")
    if not host.startswith(("https://", "http://")):
        host = f"https://{host}"
    return host


def validate_volume_path(volume_path: str) -> str:
    cleaned = "/" + volume_path.strip().strip("/")
    parts = PurePosixPath(cleaned).parts

    # Expected minimum: /Volumes/<catalog>/<schema>/<volume>
    if len(parts) < 5 or parts[1] != "Volumes":
        raise ValueError(
            "--volume-path must use this format: "
            "/Volumes/<catalog>/<schema>/<volume>/<optional-folder>"
        )
    return cleaned


def response_error(response: requests.Response, action: str) -> UploadError:
    try:
        details = response.json()
    except ValueError:
        details = response.text.strip() or "No response body"

    return UploadError(
        f"Databricks could not {action}. "
        f"HTTP {response.status_code}: {details}"
    )


def create_directory(
    session: requests.Session,
    host: str,
    directory_path: str,
) -> None:
    encoded_path = quote(directory_path, safe="/")
    url = f"{host}/api/2.0/fs/directories{encoded_path}"
    response = session.put(url, timeout=60)

    if response.status_code not in {200, 201, 204, 409}:
        raise response_error(response, f"create directory {directory_path}")


def file_chunks(file_path: Path):
    with file_path.open("rb") as source:
        while chunk := source.read(CHUNK_SIZE):
            yield chunk


def upload_file(
    session: requests.Session,
    host: str,
    local_file: Path,
    remote_file: str,
    overwrite: bool,
) -> None:
    encoded_path = quote(remote_file, safe="/")
    url = f"{host}/api/2.0/fs/files{encoded_path}"

    response = session.put(
        url,
        params={"overwrite": str(overwrite).lower()},
        data=file_chunks(local_file),
        headers={"Content-Type": "application/octet-stream"},
        timeout=(30, 1800),
    )

    if response.status_code not in {200, 201, 204}:
        raise response_error(response, f"upload {local_file.name}")


def print_query_examples(remote_file: str, extension: str) -> None:
    escaped_path = remote_file.replace("'", "''")

    print("\nUpload completed successfully.")
    print(f"Databricks path: {remote_file}")

    if extension == ".csv":
        print(
            "\nPySpark query:\n"
            f'df = (spark.read.option("header", True)\n'
            f'           .option("inferSchema", True)\n'
            f'           .csv("{remote_file}"))\n'
            "display(df)"
        )
        print(
            "\nSQL query:\n"
            f"SELECT * FROM read_files('{escaped_path}', "
            "format => 'csv', header => true);"
        )
    elif extension in {".json", ".jsonl"}:
        print(
            "\nPySpark query:\n"
            f'df = spark.read.json("{remote_file}")\n'
            "display(df)"
        )
        print(
            "\nSQL query:\n"
            f"SELECT * FROM read_files('{escaped_path}', format => 'json');"
        )
    elif extension == ".parquet":
        print(
            "\nPySpark query:\n"
            f'df = spark.read.parquet("{remote_file}")\n'
            "display(df)"
        )
        print(
            "\nSQL query:\n"
            f"SELECT * FROM read_files('{escaped_path}', format => 'parquet');"
        )


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Upload CSV, JSON, JSONL, or Parquet to a Databricks Volume."
    )
    parser.add_argument(
        "--file",
        required=True,
        help="Full path of the local file to upload.",
    )
    parser.add_argument(
        "--volume-path",
        required=True,
        help=(
            "Destination directory, for example "
            "/Volumes/main/default/tinitiate_data/bronze"
        ),
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Replace the destination file if it already exists.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_arguments()

    host = os.getenv("DATABRICKS_HOST", "").strip()
    token = os.getenv("DATABRICKS_TOKEN", "").strip()

    if not host:
        print("ERROR: Set the DATABRICKS_HOST environment variable.", file=sys.stderr)
        return 2
    if not token:
        print("ERROR: Set the DATABRICKS_TOKEN environment variable.", file=sys.stderr)
        return 2

    local_file = Path(args.file).expanduser().resolve()
    if not local_file.is_file():
        print(f"ERROR: Local file not found: {local_file}", file=sys.stderr)
        return 2

    extension = local_file.suffix.lower()
    if extension not in SUPPORTED_EXTENSIONS:
        allowed = ", ".join(sorted(SUPPORTED_EXTENSIONS))
        print(f"ERROR: Supported file extensions are: {allowed}", file=sys.stderr)
        return 2

    try:
        host = normalize_host(host)
        volume_directory = validate_volume_path(args.volume_path)
        remote_file = str(PurePosixPath(volume_directory) / local_file.name)

        session = requests.Session()
        session.headers.update({"Authorization": f"Bearer {token}"})

        create_directory(session, host, volume_directory)
        upload_file(
            session=session,
            host=host,
            local_file=local_file,
            remote_file=remote_file,
            overwrite=args.overwrite,
        )
        print_query_examples(remote_file, extension)
        return 0

    except (requests.RequestException, UploadError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
