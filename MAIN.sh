#!/bin/bash

set -e

# Activate the virtual environment for python scripts
source /home/pi/venvs/opencv-env/bin/activate

# Wakeup interval
# ie. '3600' sets wakeup at the top of every hour
#     '600' sets wakeup at ~:00, ~:10, ~:20 etc
#     '300' sets wakeup at ~:00, ~:05, ~:10, ~:15 etc
WAKEUP_INTERVAL=240

# Log file for debug information
LOG_FILE=/home/pi/powercontrol.log

# Request rtc_time from sugar
response=$(echo "get rtc_time" | nc -q 0 127.0.0.1 8423 2>&1)

if [[ $response =~ "rtc_time: " ]]; then
    echo "rtc_rtc2pi" | nc -q 0 127.0.0.1 8423 # sync sugar's rtc time to pi's clock

    rtc_time=${response#*"rtc_time: "} # trim 'rtc_time: ' off the rtc time string
    echo "Sugar rtc time: $rtc_time" | tee -a $LOG_FILE

    # Keep the full datetime format including timezone
    current_time="$rtc_time"

    # Convert current time to seconds since epoch, considering the timezone
    current_epoch=$(date --date="$current_time" +%s)

    # Calculate the next wakeup time in seconds since epoch
    next_wakeup_epoch=$((current_epoch - current_epoch % WAKEUP_INTERVAL + WAKEUP_INTERVAL))

    # Properly adjust the calculation to consider local timezone
    timezone=$(echo $rtc_time | grep -oE '[-+][0-9]{2}:[0-9]{2}$') # Extracts timezone like '-07:00'
    wakeup_time=$(date --date="@$next_wakeup_epoch" +"%Y-%m-%dT%H:%M:%S.000")$timezone # Avoid using -u to keep local time

    echo "Next calculated wakeup: $wakeup_time" | tee -a $LOG_FILE

    # Send the alarm set command to sugar
    echo "rtc_alarm_set ${wakeup_time} 0" | nc -q 0 127.0.0.1 8423

    # Double check the set time
    alarm_time=$(echo "get rtc_alarm_time" | nc -q 0 127.0.0.1 8423)
    echo "Set wakeup time is $alarm_time - (note ymd is ignored)" | tee -a $LOG_FILE # ymd is ignored and alarm is set for the current day

    # sudo /home/pi/venvs/opencv-env/bin/python3 main.py
    # sudo shutdown now

else
    echo "Failed to retrieve valid rtc_time from response: $response" | tee -a $LOG_FILE
    exit 1
fi

