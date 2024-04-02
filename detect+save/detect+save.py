import cv2
import os
import numpy as np
import time

setthreshold = 13   # Abs difference threshold
setblursize = 21    # Width of gaussian blur
setavgframes = 5    # Number of frames averaged each check
triggerdelay = 1.5  # Delay in seconds to confirm motion
vidlength = 6       # Length of the video

# Set environment variable for the current process and any subprocesses it spawns
os.environ['QT_QPA_PLATFORM'] = 'offscreen'

# Use the first camera as video source
cap = cv2.VideoCapture(0)
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

# Initialize a list to hold the last 'setavgframes' frames
frames = []

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*"avc1")
out = cv2.VideoWriter('video.mp4', fourcc, 30.0, (frame_width, frame_height))

try:
    # Read initial frames and fill the buffer
    for _ in range(setavgframes):
        done, frame = cap.read()
        if not done:
            break
        frames.append(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))  # Store gray frames

    recording = False
    record_start_time = None

    while done:
        # Calculate average of the frames in the buffer
        avg_frame = np.mean(frames, axis=0).astype(np.uint8)

        # Read the next frame
        done, NextFrame = cap.read()
        if not done:
            break
        NextGray = cv2.cvtColor(NextFrame, cv2.COLOR_BGR2GRAY)

        # Update the frames buffer
        frames.pop(0)  # Remove the oldest frame
        frames.append(NextGray)  # Add the new frame

        # Calculate the absolute difference between the average frame and the next frame
        diff = cv2.absdiff(avg_frame, NextGray)

        # Apply GaussianBlur
        blured_img = cv2.GaussianBlur(diff, (setblursize, setblursize), 0)

        # Apply threshold
        threshold, binary_img = cv2.threshold(blured_img, setthreshold, 255, cv2.THRESH_BINARY)

        # Dilate the image
        dilated = cv2.dilate(binary_img, None, iterations=12)

        # Find contours
        contours, hierarchy = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        motion_detected = False  # Flag to check if motion is detected
        for contour in contours:
            if cv2.contourArea(contour) < 1000:
                continue
            motion_detected = True
            break

        # Check motion detection state and handle recording logic
        if motion_detected:
            if not recording:
                # Start recording
                recording = True
                record_start_time = time.time()
            elif recording and (time.time() - record_start_time > triggerdelay):
                # Confirm continued motion detection
                if not motion_detected:
                    # Stop and discard the recording
                    out.release()
                    os.remove('video.mp4')
                    recording = False
                    print("Video discarded due to lack of continued motion.")
                elif time.time() - record_start_time >= vidlength:
                    # Stop recording after the specified video length
                    recording = False
                    print("Video saved.")
                    break
            if recording:
                out.write(NextFrame)

except KeyboardInterrupt:
    print("Interrupted by user")

finally:
    cap.release()
    if recording:
        out.release()