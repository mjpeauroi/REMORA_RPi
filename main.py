#!/home/pi/venvs/opencv-env/bin/python

import time
import os
import sys
import numpy 
print(f"RUNNING WITH INTERPRETER: {sys.executable}")

from get_batt import get_battery_status
from split_and_send import split, send, send_message
from motion_capture import motion_capture

working_directory = '/home/pi/Documents/REMORA_RPi'
os.chdir(working_directory)

if __name__ == "__main__":
    # Get the current battery level and send it to the spotter
    batt_level = get_battery_status()
    send_message(batt_level)
    time.sleep(1)

    print("Starting motion detection...")
    capture = motion_capture(8)
    if capture.any():
        split(capture)
        time.sleep(1)
        send()

    print("Main file ending.")
    time.sleep(1)
