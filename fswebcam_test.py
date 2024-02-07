# Experimenting with fswebcam controls


import subprocess
#import cv2 as cv
import time

#### Uncomment to get camera information
# get_camera_info_long = "lsusb -s 001:004 -v"
# get_camera_info = "v4l2-ctl --device=/dev/video0 --list-ctrls"
# subprocess.run(get_camera_info, shell=True)

### Uncomment to take photos
change_setting1 = "v4l2-ctl --device=/dev/video0 --set-ctrl=saturation=0"
subprocess.run(change_setting1, shell=True)
time.sleep(0.5)
take_photo1 = "fswebcam -r 1920x1080 --no-banner ~/Documents/camera_testing/image1.jpg"
subprocess.run(take_photo1, shell=True)
time.sleep(0.5)
change_setting2 = "v4l2-ctl --device=/dev/video0 --set-ctrl=saturation=56"
subprocess.run(change_setting2, shell=True)
time.sleep(0.5)
take_photo2 = "fswebcam -r 1920x1080 --no-banner ~/Documents/camera_testing/image2.jpg"
subprocess.run(take_photo2, shell=True)
time.sleep(0.5)


### Uncomment either to take a video
take_video = [
    "ffmpeg",
    "-y",                          # Overwrite output files without asking
    "-t", "6",                    # Duration
    "-f", "video4linux2",          # Input format
    "-i", "/dev/video0",           # Input device (webcam)
    "-s", "1920x1080",             # Video size
    "-c:v", "h264",                # Video codec
    "-pix_fmt", "yuv420p",         # Pixel format
    "video.mp4"                    # Output file
]
# subprocess.run(take_video)

# take_5s_video = "ffmpeg -y -t 5 -f video4linux2 -i /dev/video0 -s 1920x1080 -c:v h264 -pix_fmt yuv420p video.mp4"
# subprocess.run(take_5s_video, shell=True)
