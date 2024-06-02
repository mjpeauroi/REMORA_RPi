#!/bin/bash

set -e

# Wakeup interval
# ie. '3600' sets wakeup at the top of every hour
#     '600' sets wakeup at ~:00, ~:10, ~:20 etc
#     '300' sets wakeup at ~:00, ~:05, ~:10, ~:15 etc
WAKEUP_INTERVAL=300

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

else
    echo "Failed to retrieve valid rtc_time from response: $response" | tee -a $LOG_FILE
    exit 1
fi





#     # Set the system time using the date command directly from ISO8601 format
#     if sudo date -u -s "$rtc_time"; then
#         echo "System time set to: $(date)" | tee -a $LOG_FILE
#     else
#         echo "Failed to set system time" | tee -a $LOG_FILE
#         exit 1
#     fi

#     # Calculate the next wakeup time (3 minutes from current RTC time)
#     wakeup_time=$(date -d "$rtc_time + 3 minutes" +%Y-%m-%dT%H:%M:%S%:z)
#     echo "Calculated wakeup time is $wakeup_time" | tee -a $LOG_FILE

#     # Set the RTC alarm
#     command="rtc_alarm_set ${wakeup_time} 127"
#     echo "Sending command: $command" | tee -a $LOG_FILE
#     r=$(echo "$command" | nc -q 0 127.0.0.1 8423)
#     echo "RTC Alarm Set Response: $r" | tee -a $LOG_FILE

#     # Check if the alarm was set correctly
#     alarm_time=$(echo "get rtc_alarm_time" | nc -q 0 127.0.0.1 8423)
#     echo "Set wakeup time is $alarm_time" | tee -a $LOG_FILE

#     # Remove milliseconds for comparison
#     alarm_time=${alarm_time#*" "}
#     alarm_time=${alarm_time%.*}

#     # Detailed logging for comparison
#     echo "Expected wakeup time: $wakeup_time" | tee -a $LOG_FILE
#     echo "Retrieved alarm time: $alarm_time" | tee -a $LOG_FILE

#     if [[ $alarm_time == "$wakeup_time" ]]; then
#         # Sleep for n seconds then poweroff
#         echo "Sleeping for $SHUTDOWN_AFTER seconds before shutdown" | tee -a $LOG_FILE
#         sleep $SHUTDOWN_AFTER
#         sudo shutdown now
#     else
#         echo "Set RTC wakeup time error: $alarm_time did not match $wakeup_time" | tee -a $LOG_FILE
#         exit 1
#     fi
# else
#     echo "Get RTC time error" | tee -a $LOG_FILE
#     exit 1
# fi