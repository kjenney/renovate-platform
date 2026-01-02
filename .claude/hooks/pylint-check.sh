#!/bin/bash
# PostToolUse hook for running pylint on edited/written Python files

# Read JSON from stdin and extract file path
FILE=$(cat | jq -r '.tool_input.file_path // empty')

# Only run pylint on Python files
if [[ "$FILE" == *.py ]]; then
    pylint "$FILE" --exit-zero 2>/dev/null || true
fi
