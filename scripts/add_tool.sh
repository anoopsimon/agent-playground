#!/usr/bin/env bash
set -euo pipefail

ROUTES_FILE="app/routes.py"

if [ ! -f "$ROUTES_FILE" ]; then
  echo "Cannot find $ROUTES_FILE"
  exit 1
fi

read -r -p "Tool name (snake_case, e.g., my_tool): " TOOL_NAME
if [ -z "$TOOL_NAME" ]; then
  echo "Tool name is required."
  exit 1
fi
if ! [[ "$TOOL_NAME" =~ ^[a-zA-Z_][a-zA-Z0-9_]*$ ]]; then
  echo "Invalid tool name. Use letters, numbers, and underscores."
  exit 1
fi

read -r -p "Tool description: " TOOL_DESC
if [ -z "$TOOL_DESC" ]; then
  echo "Tool description is required."
  exit 1
fi

PARAM_LINES=()
while true; do
  read -r -p "Param name (blank to finish): " PNAME
  if [ -z "$PNAME" ]; then
    break
  fi
  read -r -p "Param type [string|integer|number|boolean] (default: string): " PTYPE
  if [ -z "$PTYPE" ]; then
    PTYPE="string"
  fi
  read -r -p "Param description: " PDESC
  PARAM_LINES+=("${PNAME}|${PTYPE}|${PDESC}")
done

PARAMS_JOINED="$(printf "%s\n" "${PARAM_LINES[@]}")"
export TOOL_NAME TOOL_DESC PARAMS_JOINED

python - <<'PY'
import os
import re
from textwrap import indent

routes_file = "app/routes.py"
tool_name = os.environ["TOOL_NAME"]
tool_desc = os.environ["TOOL_DESC"]
params_joined = os.environ.get("PARAMS_JOINED", "")

param_entries = []
for line in params_joined.splitlines():
    if not line.strip():
        continue
    name, ptype, pdesc = line.split("|", 2)
    param_entries.append((name.strip(), ptype.strip(), pdesc.strip()))

with open(routes_file, "r", encoding="utf-8") as f:
    content = f.read()

if re.search(rf'name="{re.escape(tool_name)}"', content):
    raise SystemExit(f"Tool '{tool_name}' already exists in {routes_file}.")

func_name = f"{tool_name}_tool"
if param_entries:
    args = ", ".join([p[0] for p in param_entries])
    params_body = ",\n".join(
        [f'"{n}": {{"type": "{t}", "description": "{d}"}}' for n, t, d in param_entries]
    )
else:
    args = ""
    params_body = ""

func_block = [
    f"def {func_name}({args}):",
    f'    return "TODO: implement {tool_name}"',
    "",
    "register_tool(Tool(",
    f'    name="{tool_name}",',
    f'    description="{tool_desc}",',
    "    parameters={",
]
if params_body:
    func_block.append(indent(params_body, " " * 8))
func_block += [
    "    },",
    f"    func={func_name}",
    "))",
    "",
]
snippet = "\n".join(func_block)

marker = "# --- API endpoints ---"
if marker not in content:
    raise SystemExit(f"Could not find marker '{marker}' in {routes_file}.")

new_content = content.replace(marker, snippet + marker)

with open(routes_file, "w", encoding="utf-8") as f:
    f.write(new_content)
PY

echo "Tool '$TOOL_NAME' added to $ROUTES_FILE."
