#!/home/pi/venvs/opencv-env/bin/python

import cv2
import os
import numpy as np
import time

setthreshold = 60
setblursize = 51
setsize = 3000
setavgframes = 20
compression_quality = 90

def motion_capture():
    os.environ['QT_QPA_PLATFORM'] = 'offscreen'
    cap = cv2.VideoCapture(0)
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))

    time.sleep(2)  # Allow auto-exposure to settle

    directory_path = os.path.expanduser('~/Documents/REMORA_RPi/motiontest/')
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
    files = os.listdir(directory_path)
    image_index = len(files)

    frames = []

    try:
        for _ in range(setavgframes):
            done, frame = cap.read()
            if not done:
                print("Failed to capture initial frames")
                return
            frames.append(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))

        while True:
            avg_frame = np.mean(frames, axis=0).astype(np.uint8)
            done, NextFrame = cap.read()
            if not done:
                print("Failed to read next frame")
                break
            NextGray = cv2.cvtColor(NextFrame, cv2.COLOR_BGR2GRAY)
            frames.pop(0)
            frames.append(NextGray)
            diff = cv2.absdiff(avg_frame, NextGray)
            blured_img = cv2.GaussianBlur(diff, (setblursize, setblursize), 0)
            threshold, binary_img = cv2.threshold(blured_img, setthreshold, 255, cv2.THRESH_BINARY)
            dilated = cv2.dilate(binary_img, None, iterations=12)
            contours, hierarchy = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

            for contour in contours:
                if cv2.contourArea(contour) >= setsize:
                    for wait in range(3):
                        time.sleep(1)
                        capture_time = time.time()  # Capture the current time
                        done, image = cap.read()
                        if not done:
                            print("Failed to capture image during motion capture sequence")
                            break
                        image_path = f"{directory_path}img_{image_index}_{wait}.jpg"
                        cv2.imwrite(image_path, image, [int(cv2.IMWRITE_JPEG_QUALITY), compression_quality])
                        print(f"Motion detected and image saved as {image_path}, time elapsed: {capture_time:.2f} seconds")
                        image_index += 1
                    return  # Exit after capturing three images on motion

    except KeyboardInterrupt:
        print("Interrupted by user")

    finally:
        cap.release()
        print("Camera released and program ended")

if __name__ == '__main__':
    motion_capture()