#!/usr/bin/env bash
set -euo pipefail

PYTHON_BIN="python3"
if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  PYTHON_BIN="python"
fi

mapfile -t FILES < <(
  "$PYTHON_BIN" - <<'PY'
import subprocess

out = subprocess.check_output(["git", "status", "--porcelain", "-z"])
parts = out.split(b"\x00")
paths = []
for entry in parts:
    if not entry:
        continue
    status = entry[:2]
    payload = entry[3:]
    if not payload:
        continue
    if status.startswith(b"R") or status.startswith(b"C"):
        # For renames/copies, the next entry is the new path.
        continue
    paths.append(payload.decode("utf-8"))
print("\n".join(paths))
PY
)

if [ "${#FILES[@]}" -eq 0 ]; then
  echo "No changes to commit."
  exit 0
fi

echo "Found ${#FILES[@]} changed file(s):"
for f in "${FILES[@]}"; do
  echo "- $f"
done

for file in "${FILES[@]}"; do
  read -r -p "Commit message for ${file}: " msg
  if [ -z "${msg}" ]; then
    echo "Commit message is required."
    exit 1
  fi
  git add "$file"
  git commit -m "$msg"
done
