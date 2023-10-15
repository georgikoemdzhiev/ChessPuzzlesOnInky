#!/bin/bash

set -e

# Get the directory of the Bash script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Command to execute the Python script
PYTHON_CMD="python3 $SCRIPT_DIR/main.py"

# Check if the user has a crontab already
if [ "$(crontab -l 2>/dev/null | wc -l)" -eq 0 ]; then
    # No existing crontab, so create one
    # Change the working directory so that we can load the custom fonts
    echo "0 8 * * * cd $SCRIPT_DIR && $PYTHON_CMD" | crontab -
else
    # User already has a crontab, just add the new job
    (crontab -l ; echo "0 8 * * * $PYTHON_CMD") | crontab -
fi

echo "Cron job setup completed successfully!"