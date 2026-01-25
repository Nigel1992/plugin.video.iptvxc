#!/usr/bin/env bash
# Build a release zip for the addon with a clean, minimal set of files.
# Usage: ./scripts/build_release.sh 3.4.0
set -euo pipefail
VERSION=${1:-3.4.0}
ADDON_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PARENT_DIR="$(dirname "$ADDON_DIR")"
OUT="${PARENT_DIR}/plugin.video.iptvxc-${VERSION}.zip"
cd "$PARENT_DIR"
# Exclude common development and cache artifacts
EXCLUDE=(
  "plugin.video.iptvxc/*.pyc"
  "plugin.video.iptvxc/__pycache__/*"
  "plugin.video.iptvxc/.git/*"
  "plugin.video.iptvxc/.github/*"
  "plugin.video.iptvxc/*.zip"
  "plugin.video.iptvxc/*.code-workspace"
  "plugin.video.iptvxc/.DS_Store"
  "plugin.video.iptvxc/.vscode/*"
  "plugin.video.iptvxc/*.swp"
  "plugin.video.iptvxc/*.log"
  "plugin.video.iptvxc/node_modules/*"
  "plugin.video.iptvxc/tests/*"
)
# Build exclusion args for zip
EX_ARGS=()
for p in "${EXCLUDE[@]}"; do
  EX_ARGS+=( -x "$p" )
done
# Ensure previous build removed
rm -f "$OUT"
# Create zip with top-level folder present
zip -r "$OUT" plugin.video.iptvxc "${EX_ARGS[@]}"

# Remove any residual unwanted paths that zip still included (eg empty dirs)
zip -d "$OUT" "plugin.video.iptvxc/.git/*" "plugin.video.iptvxc/__pycache__/*" "plugin.video.iptvxc/scripts/*" "plugin.video.iptvxc/test-logos/*" "plugin.video.iptvxc/*.pyc" || true

# Print summary
echo "Created $OUT"
echo "Contents:"
unzip -l "$OUT" | sed -n '1,200p'
