#!/usr/bin/env bash
# Rerun of results/2026_deepseek_flash_guideline (harsh + Strength Finder, all
# deepseek-v4-flash) on all 400 papers, using that run's snapshot code/prompts
# since current code/ has the neutral reviewer disabled.

set -e
cd "$(dirname "$0")/.."

SRC_SNAPSHOT="results/2026_deepseek_flash_guideline/snapshot"

export ANTHROPIC_API_KEY=""
export OPENAI_DEFAULT_MODEL="glm-5.1"
export HARSH_MODEL="deepseek-v4-flash"
export MERGER_MODEL="deepseek-v4-flash"
export NEUTRAL_MODEL="deepseek-v4-flash"
export SWEEP_NAME="${SWEEP_NAME:-2026_deepseek_flash_guideline_v2}"
export OUTPUT_CSV="${SWEEP_NAME}/scores.csv"
export MERGE_LOG="${SWEEP_NAME}/merge.log"
export CONCURRENCY="${CONCURRENCY:-30}"
export MAX_PAPERS="${MAX_PAPERS:-400}"
export CALIBRATION_SET="deepreview"
export PAPERS_DIR="${PAPERS_DIR:-$HOME/split_review/datasets/iclr2026_new/papers}"
export REVIEWS_DIR="${SWEEP_NAME}/reviews"
export OPENROUTER_PROVIDER="${OPENROUTER_PROVIDER:-"deepseek"}"
export REVIEW_RESULTS_DIR="$PWD/results"
export REVIEW_PROMPTS_DIR="$PWD/$SRC_SNAPSHOT/prompts"

LOG_FILE="results/${MERGE_LOG}"
mkdir -p "$(dirname "$LOG_FILE")"

SNAPSHOT_DIR="results/${SWEEP_NAME}/snapshot"
if [ -e "$SNAPSHOT_DIR" ]; then
  echo "ERROR: $SNAPSHOT_DIR already exists. Bump SWEEP_NAME." >&2
  exit 1
fi
mkdir -p "$SNAPSHOT_DIR"
cp -r "$SRC_SNAPSHOT/code" "$SRC_SNAPSHOT/prompts" "$SNAPSHOT_DIR/"
cp scripts/run_deepreview_neutral_v2.sh "$SNAPSHOT_DIR/"
echo "rerun of $SRC_SNAPSHOT" > "$SNAPSHOT_DIR/git_commit.txt"

{
  echo "============================================================"
  echo "Config @ $(date '+%Y-%m-%dT%H:%M:%S')"
  echo "SNAPSHOT=${SNAPSHOT_DIR} (code/prompts copied from ${SRC_SNAPSHOT})"
  echo "OPENAI_DEFAULT_MODEL=$OPENAI_DEFAULT_MODEL"
  echo "HARSH_MODEL=$HARSH_MODEL"
  echo "MERGER_MODEL=$MERGER_MODEL"
  echo "NEUTRAL_MODEL=$NEUTRAL_MODEL"
  echo "SWEEP_NAME=$SWEEP_NAME"
  echo "OUTPUT_CSV=$OUTPUT_CSV"
  echo "MERGE_LOG=$MERGE_LOG"
  echo "CONCURRENCY=$CONCURRENCY"
  echo "MAX_PAPERS=$MAX_PAPERS"
  echo "CALIBRATION_SET=$CALIBRATION_SET"
  echo "PAPERS_DIR=$PAPERS_DIR"
  echo "REVIEWS_DIR=$REVIEWS_DIR"
  echo "OPENROUTER_PROVIDER=$OPENROUTER_PROVIDER"
} >> "$LOG_FILE"

python "$SRC_SNAPSHOT/code/main.py" --n_samples "$MAX_PAPERS" --benchmark "$PAPERS_DIR/.." --seed $(cksum <<< '2343' | cut -f 1 -d ' ')
