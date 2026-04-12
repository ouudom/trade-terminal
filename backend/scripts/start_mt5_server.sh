#!/usr/bin/env bash
# Start the mt5linux socket server under Wine Python.
# Must be running before uvicorn starts.
#
# Usage:
#   ./scripts/start_mt5_server.sh
#
# Override host/port via env:
#   MT5_HOST=127.0.0.1 MT5_PORT=18812 ./scripts/start_mt5_server.sh

set -e

HOST="${MT5_HOST:-127.0.0.1}"
PORT="${MT5_PORT:-18812}"

echo "[mt5linux] Starting socket server on ${HOST}:${PORT} ..."
wine python -c "from mt5linux import server; server.run(host='${HOST}', port=${PORT})"
