#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
REPO_ROOT=$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)
SRC_DIR="$REPO_ROOT/third_party/displayplacer/src"
BIN_DIR="$REPO_ROOT/bin"
TARGET="$BIN_DIR/displayplacer"

if [ "$(uname -s)" != "Darwin" ]; then
  echo "This bootstrap script only supports macOS." >&2
  exit 1
fi

if ! command -v make >/dev/null 2>&1; then
  echo "Missing \`make\`. Install Xcode Command Line Tools or Xcode first." >&2
  exit 1
fi

if ! command -v cc >/dev/null 2>&1; then
  echo "Missing \`cc\`. Install Xcode Command Line Tools or Xcode first." >&2
  exit 1
fi

mkdir -p "$BIN_DIR"

echo "Building vendored displayplacer..."
make -C "$SRC_DIR"
cp "$SRC_DIR/displayplacer" "$TARGET"
chmod +x "$TARGET"

echo "Built: $TARGET"
