# REMORA_RPi
Raspberry Pi code for the Remora system.

Local code is found at [REMORA_Local](https://github.com/mjpeauroi/REMORA_Local)

# Some notes:
OpenCV could not be installed to root, so we need to make a venv
MAIN.sh automatically activates the venv but if you're running any script by itself, be sure to activate:
source /home/pi/venvs/opencv-env/bin/activate (with with path for your specific venv)

Full automation requires you set up a systemd file to run the bash script on boot. Accessing service file may look something like:
sudo nano /etc/systemd/system/powercontrol.service

With contents something like the following:

[Unit]
Description=Sleep/Wake Cycle

After=network.target

[Service]
ExecStart=/home/pi/Documents/REMORA_RPi/MAIN.sh  # replace with the location of your master bash file

Restart=on-failure

User=root

StandardOutput=append:/home/pi/Documents/REMORA_RPi/LOG.log  # replace with desired log file location

StandardError=inherit

[Install]
WantedBy=multi-user.target

Other scripts used for testing/work in progress are found in test_script_archive

# Helpful code snips
To enable, start, and check the run status of the bash script automation service paste this:
sudo systemctl enable powercontrol.service
sudo systemctl start powercontrol.service
sudo systemctl status powercontrol.service

To disable it paste this (keep this handy in case shutdown is scheduled soon after wakeup):
sudo systemctl stop powercontrol.service
sudo systemctl disable powercontrol.service

Here's some nice tester commands I found useful for testing via CLI:
(Reference [pisugar-power-manager github](https://github.com/PiSugar/pisugar-power-manager-rs))

wakeup_time=$(date -d "+2 minutes" --iso-8601=seconds)

echo "Wakeup time is set to: $wakeup_time"

echo "rtc_alarm_set ${wakeup_time} 127" | nc -q 0 127.0.0.1 8423

alarm_time=$(echo "get rtc_alarm_time" | nc -q 0 127.0.0.1 8423)

echo "Set wakeup time is $alarm_time"

