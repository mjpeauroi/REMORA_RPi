## MSI Remora code for Raspberry Pi


# OpenCV cannot be installed to root, so we needed to make a venv
# MAIN.sh automatically activates this but if you're running any script by itself, be sure to activate:
source /home/pi/venvs/opencv-env/bin/activate

# You  need to set up a systemd file to run the bash script on boot
sudo nano /etc/systemd/system/powercontrol.service
# Something like the following:
[Unit]
Description=Sleep/Wake Cycle
After=network.target

[Service]
ExecStart=/home/pi/Documents/REMORA_RPi/MAIN.sh
Restart=on-failure
User=root
StandardOutput=append:/home/pi/Documents/REMORA_RPi/LOG.log
StandardError=inherit

[Install]
WantedBy=multi-user.target


# To enable, start, and check the run status of the service paste this
sudo systemctl enable powercontrol.service
sudo systemctl start powercontrol.service
sudo systemctl status powercontrol.service

# And to disable it paste this (keep this handy in case it shuts down fast)
sudo systemctl stop powercontrol.service
sudo systemctl disable powercontrol.service

# Here's some nice tester commands you can run from cmd line to test setting wakeups:
# Reference pisugar-power-manager github for more
wakeup_time=$(date -d "+2 minutes" --iso-8601=seconds)
echo "Wakeup time is set to: $wakeup_time"
echo "rtc_alarm_set ${wakeup_time} 127" | nc -q 0 127.0.0.1 8423
alarm_time=$(echo "get rtc_alarm_time" | nc -q 0 127.0.0.1 8423)
echo "Set wakeup time is $alarm_time"

