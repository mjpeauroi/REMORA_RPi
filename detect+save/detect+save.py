import cv2
import os
import numpy as np
import time

setthreshold = 90  # Abs difference threshold
setblursize = 41  # Width of gaussian blur
setavgframes = 7  # Number of frames averaged each check
triggerdelay = 1.5  # Delay in seconds to confirm motion
vidlength = 6  # Length of the video in seconds

# Specify no viewing platform
os.environ['QT_QPA_PLATFORM'] = 'offscreen'

working_directory = os.path.expanduser('~/Documents/REMORA_RPi/detect+save')
os.chdir(working_directory)

def main():
    cam = cv2.VideoCapture(0)
    frame_width = int(cam.get(3))
    frame_height = int(cam.get(4))

    os.makedirs("videos", exist_ok=True)
    directory_path = os.path.expanduser('~/Documents/REMORA_RPi/detect+save/videos/')
    files = os.listdir(directory_path)
    index = len(files) + 1

    fourcc = cv2.VideoWriter_fourcc(*"avc1")
    out = cv2.VideoWriter(f'{directory_path}video_{index}.mp4', fourcc, 15.0, (frame_width, frame_height))

    frames = []

    # initially fill the buffer
    for _ in range(setavgframes):
        done, frame = cam.read()
        if not done:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurredgray = cv2.GaussianBlur(gray, (setblursize, setblursize), 0)
        frames.append(blurredgray)

    avg_frame = np.mean(frames, axis=0)
    recording = False
    start_time = None

    try:
        while True:
            done, next_frame = cam.read()
            if not done:
                break

            if recording:
                out.write(next_frame)
                elapsed_time = time.time() - start_time
                if elapsed_time >= vidlength:
                    recording = False
                    out.release()
                    print(f"Video {index} saved.")
                    index += 1
                    out = cv2.VideoWriter(f'{directory_path}video_{index}.mp4', fourcc, 15.0, (frame_width, frame_height))
                    continue  # Move to the next iteration to avoid additional logic in this loop

            gray_next = cv2.cvtColor(next_frame, cv2.COLOR_BGR2GRAY)
            blurredgray_next = cv2.GaussianBlur(gray_next, (setblursize, setblursize), 0)
            frame_delta = cv2.absdiff(avg_frame.astype(np.uint8), blurredgray_next)
            thresh = cv2.threshold(frame_delta, setthreshold, 255, cv2.THRESH_BINARY)[1]
            thresh = cv2.dilate(thresh, None, iterations=2)
            contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            if any(cv2.contourArea(contour) > 1000 for contour in contours):
                if not recording:
                    start_time = time.time()
                    recording = True
                    print(f"Recording for {index} started")
            else:
                if recording:
                    # Consider moving the stopping logic here if needed
                    pass

    except KeyboardInterrupt:
        print("Interrupted by user")

    finally:
        cam.release()
        if recording:
            out.release()

if __name__ == "__main__":
    main()
