import cv2
import os
import numpy as np

setthreshold = 13
setblursize = 21
setavgframes = 20

# Set environment variable for the current process and any subprocesses it spawns
os.environ['QT_QPA_PLATFORM'] = 'offscreen'

# Use the first camera as video source
cap = cv2.VideoCapture(0)

# Initialize a list to hold the last 'setavgframes' frames
frames = []

try:
    # Read initial frames and fill the buffer
    for _ in range(setavgframes):
        done, frame = cap.read()
        if not done:
            break
        frames.append(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))  # Store gray frames

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
            print("Motion detected")

        if not motion_detected:
            # If no motion is detected
            print("No motion detected")

except KeyboardInterrupt:
    print("Interrupted by user")

finally:
    cap.release()
