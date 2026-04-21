#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

bash "$SCRIPT_DIR/run_mode_area_rca8.sh"
bash "$SCRIPT_DIR/run_mode_delay_rca8.sh"
bash "$SCRIPT_DIR/run_mode_balanced_rca8.sh"

echo "All Part 3 modes complete."
