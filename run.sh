#!/data/data/com.termux/files/usr/bin/bash
# Run from inside the proxybot folder: bash run.sh
cd "$(dirname "$0")"

# Load .env into the environment
if [ -f .env ]; then
  set -a
  source .env
  set +a
else
  echo ".env file not found. Create it first (see README)."
  exit 1
fi

source venv/bin/activate
python bot.py
