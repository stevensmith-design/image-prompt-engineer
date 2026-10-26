#!/bin/sh
# Package the skill as dist/image-prompt-engineer.skill for upload to Claude.ai or Claude Desktop.
set -e
cd "$(dirname "$0")"
mkdir -p dist
rm -f dist/image-prompt-engineer.skill
zip -rq dist/image-prompt-engineer.skill image-prompt-engineer -x '*/__pycache__/*' '*.DS_Store'
echo "Built dist/image-prompt-engineer.skill"
