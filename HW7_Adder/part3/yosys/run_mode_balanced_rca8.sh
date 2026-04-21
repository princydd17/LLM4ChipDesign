#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ENV="${SCRIPT_DIR}/../../.env"
if [[ -f "$PROJECT_ENV" ]]; then
  set -a
  # shellcheck disable=SC1090
  source "$PROJECT_ENV"
  set +a
fi

if [[ -z "${PORTKEY_API_KEY:-}" && -z "${NYU_GATEWAY_API_KEY:-}" && -z "${OPENAI_API_KEY:-}" ]]; then
  echo "ERROR: Set PORTKEY_API_KEY or NYU_GATEWAY_API_KEY or OPENAI_API_KEY"
  exit 1
fi

if [[ -x "${SCRIPT_DIR}/../../.venv/bin/python" ]]; then
  PY="${SCRIPT_DIR}/../../.venv/bin/python"
else
  PY="python3"
fi

cd "$SCRIPT_DIR"
export MPLCONFIGDIR="${SCRIPT_DIR}/../runs/.mplconfig"
mkdir -p "$MPLCONFIGDIR"
$PY optimize_adder.py \
  --mode balanced \
  --baseline ../../part1/golden/RCA8.v \
  --top RCA8 \
  --out ../runs/mode_balanced_rca8 \
  --max-iter 10

$PY plot_ppa.py ../runs/mode_balanced_rca8/optimization_log.json \
  -o ../runs/mode_balanced_rca8/ppa_trajectory.pdf

echo "Mode C run complete: ../runs/mode_balanced_rca8"
