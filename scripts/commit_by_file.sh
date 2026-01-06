#!/usr/bin/env bash
set -euo pipefail

# Update these arrays to match the files you want to commit and the messages.
FILES=(
  "app/routes.py"
  "requirements.txt"
  ".env.example"
  "README.md"
  "scripts/commit_by_file.sh"
)

MESSAGES=(
  "Add Brave Search MCP tool"
  "Add required dependencies"
  "Document Brave API key in env example"
  "Restructure README with usage and contribution notes"
  "Add reusable commit-by-file helper script"
)

if [ "${#FILES[@]}" -ne "${#MESSAGES[@]}" ]; then
  echo "FILES and MESSAGES must have the same length."
  exit 1
fi

for i in "${!FILES[@]}"; do
  file="${FILES[$i]}"
  msg="${MESSAGES[$i]}"
  if [ ! -e "$file" ]; then
    echo "Skipping missing file: $file"
    continue
  fi
  git add "$file"
  git commit -m "$msg"
done
