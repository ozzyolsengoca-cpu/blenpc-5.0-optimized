#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

ARCHIVE_NAME="blenpc_all_files.zip"

rm -f "$ARCHIVE_NAME"
zip -r "$ARCHIVE_NAME" . \
  -x '.git/*' \
     '.pytest_cache/*' \
     '__pycache__/*' \
     '*/__pycache__/*' \
     '*.pyc'

echo "Archive created: $ROOT_DIR/$ARCHIVE_NAME"
