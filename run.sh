#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DASH_DIR="$ROOT_DIR/spotify_trends_dashboard"
SEARCH_DIR="$ROOT_DIR/5A_Search"
PYTHON_BIN="$ROOT_DIR/.venv/bin/python"
PIP_BIN="$ROOT_DIR/.venv/bin/pip"

DASH_HOST="${DASH_HOST:-127.0.0.1}"
DASH_PORT="${DASH_PORT:-8050}"
SEARCH_HOST="${SEARCH_HOST:-127.0.0.1}"
SEARCH_PORT="${SEARCH_PORT:-5173}"

export PATH="/home/ahmed/.local/nodejs/bin:$PATH"

PIDS=()

cleanup() {
  echo ""
  echo "Stopping Spotify dashboard and 5*A Search..."
  for pid in "${PIDS[@]:-}"; do
    if kill -0 "$pid" >/dev/null 2>&1; then
      kill "$pid" >/dev/null 2>&1 || true
    fi
  done
}

trap cleanup EXIT INT TERM

port_in_use() {
  "$PYTHON_BIN" -c "import socket, sys; s=socket.socket(); s.settimeout(0.3); sys.exit(0 if s.connect_ex((sys.argv[1], int(sys.argv[2]))) == 0 else 1)" "$1" "$2"
}

echo "=============================================="
echo " Spotify Trends + 5*A Search Launcher"
echo "=============================================="

if [ ! -x "$PYTHON_BIN" ]; then
  echo "Creating Python virtual environment..."
  python3 -m venv "$ROOT_DIR/.venv"
fi

if ! "$PYTHON_BIN" -c "import dash, pandas, plotly" >/dev/null 2>&1; then
  echo "Installing Python dashboard dependencies..."
  "$PIP_BIN" install -r "$DASH_DIR/requirements.txt"
fi

if [ ! -d "$SEARCH_DIR/node_modules" ]; then
  echo "Installing 5*A Search dependencies..."
  (cd "$SEARCH_DIR" && npm install)
fi

echo ""
if port_in_use "$DASH_HOST" "$DASH_PORT"; then
  echo "Dash dashboard already responds at http://$DASH_HOST:$DASH_PORT"
else
  echo "Starting Dash dashboard: http://$DASH_HOST:$DASH_PORT"
  (cd "$DASH_DIR" && "$PYTHON_BIN" app.py --host "$DASH_HOST" --port "$DASH_PORT") &
  PIDS+=("$!")
fi

if port_in_use "$SEARCH_HOST" "$SEARCH_PORT"; then
  echo "5*A Search already responds at http://$SEARCH_HOST:$SEARCH_PORT"
else
  echo "Starting 5*A Search:       http://$SEARCH_HOST:$SEARCH_PORT"
  (cd "$SEARCH_DIR" && npm run dev -- --host "$SEARCH_HOST" --port "$SEARCH_PORT") &
  PIDS+=("$!")
fi

echo ""
echo "Open these URLs:"
echo "  Dashboard: http://$DASH_HOST:$DASH_PORT"
echo "  Assistant: http://$SEARCH_HOST:$SEARCH_PORT"
echo ""
echo "Press Ctrl+C to stop both apps."

if [ "${#PIDS[@]}" -gt 0 ]; then
  wait
else
  echo "Both apps were already running. Nothing new to wait for."
fi
