#!/usr/bin/env bash
# Only sanctioned git surface: stage everything and commit with a message.
# Usage: scripts/gitsnap.sh "commit message" ["second -m line"]
set -euo pipefail

if [ "$#" -lt 1 ]; then
    echo "usage: gitsnap.sh <message> [extra -m line]" >&2
    exit 1
fi

git add -A

if git diff --cached --quiet; then
    echo "nothing to commit, working tree clean"
    exit 0
fi

if [ "$#" -ge 2 ]; then
    git commit -m "$1" -m "$2"
else
    git commit -m "$1"
fi
