#!/bin/bash

set -e

# Get the directory of the Bash script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Command to execute the Python script
PYTHON_CMD="python3 $SCRIPT_DIR/main.py"

# Schedule the cron job
(crontab -l ; echo "0 8 * * * $PYTHON_CMD") | crontab -

echo "Cron job setup completed successfully"