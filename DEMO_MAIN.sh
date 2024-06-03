#!/bin/bash

set -e

# Activate the virtual environment for Python scripts
source /home/pi/venvs/opencv-env/bin/activate

# Path to the log file
LOG_FILE="/home/pi/demo_powercontrol.log"

# Path to the flag files
FLAG_FILE="/home/pi/Documents/REMORA_RPi/first_wakeup.flag"
SECOND_FLAG_FILE="/home/pi/Documents/REMORA_RPi/second_wakeup.flag"

# Time to wake up for the first time
WAKEUP_TIME="2024-06-02T17:23:00.000-07:00"
SECOND_WAKEUP_TIME=$(date -d "$WAKEUP_TIME 5 minutes" +"%Y-%m-%dT%H:%M:%S.000-07:00")

# Check if the second flag file exists
if [ -f "$SECOND_FLAG_FILE" ]; then
    echo "Second flag file found, running the main program for the second time..." | tee -a "$LOG_FILE"
    python3 /home/pi/Documents/REMORA_RPi/main.py
    echo "Second run of main program ended." | tee -a "$LOG_FILE"
    # Clean up the second flag file
    rm "$SECOND_FLAG_FILE"
    # No more wakeups needed, end here
    exit 0
fi

# Check if the first flag file exists
if [ -f "$FLAG_FILE" ]; then
    echo "First flag file found, running the main program for the first time..." | tee -a "$LOG_FILE"
    python3 /home/pi/Documents/REMORA_RPi/main.py
    echo "First run of main program ended." | tee -a "$LOG_FILE"
    # Clean up the first flag file
    rm "$FLAG_FILE"
    # Setup for the second wakeup
    echo "Setting up second wakeup at $SECOND_WAKEUP_TIME" | tee -a "$LOG_FILE"
    echo "rtc_alarm_set $SECOND_WAKEUP_TIME 127" | nc -q 0 127.0.0.1 8423
    touch "$SECOND_FLAG_FILE"
    echo "Second flag file created at $SECOND_FLAG_FILE" | tee -a "$LOG_FILE"
    # Initiate shutdown again
    echo "Shutting down again for second wakeup..." | tee -a "$LOG_FILE"
    sleep 1
    sudo shutdown now
else
    # No flag files, first run setup logic
    echo "No flag files found, first run setup..." | tee -a "$LOG_FILE"
    echo "First wakeup: $WAKEUP_TIME" | tee -a "$LOG_FILE"
    # Send the alarm set command for the first wakeup
    echo "Setting first wakeup time..." | tee -a "$LOG_FILE"
    echo "rtc_alarm_set $WAKEUP_TIME 127" | nc -q 0 127.0.0.1 8423
    # Create a flag file to indicate that the first wakeup is set
    touch "$FLAG_FILE"
    echo "First flag file created at $FLAG_FILE" | tee -a "$LOG_FILE"
    # Initiate shutdown after setting the alarm
    echo "Shutting down now for first wakeup..." | tee -a "$LOG_FILE"
    sleep 1
    sudo shutdown now
fi
