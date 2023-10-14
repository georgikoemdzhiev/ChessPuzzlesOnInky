#!/bin/bash

# Get the directory of the Bash script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Command to execute the Python script
PYTHON_CMD="python3 $SCRIPT_DIR/main.py"

# Check if the user has a crontab already
if [ "$(crontab -l 2>/dev/null | wc -l)" -eq 0 ]; then
    # No existing crontab, so create one
    echo "0 8 * * * $PYTHON_CMD" | crontab -
    next_run="8:00 AM every day"
else
    # User already has a crontab, just add the new job
    (crontab -l ; echo "0 8 * * * $PYTHON_CMD") | crontab -
    next_run_time=$(date -d "$(crontab -l | grep "$PYTHON_CMD" | awk '{print $1, $2, $3, $4, $5}')")
    next_run=$(date -d "$next_run_time" "+%H:%M %p on %A, %B %d, %Y")
fi

# Display confirmation and the next scheduled run time
echo "Cron job successfully set up."
echo "Next scheduled run: $next_run"
