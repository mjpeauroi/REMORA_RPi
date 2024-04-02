import cv2
import numpy as np
from video_recorder import Video_Recorder

def detect_motion(frame, avg_frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    frame_delta = cv2.absdiff(avg_frame, gray)
    thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)
    contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        if cv2.contourArea(contour) > 1000:  # Motion threshold area
            return True
    return False

def main():
    cam = Video_Recorder()
    _, avg_frame = cam.get_frame()  # Get the first frame as the average frame
    avg_frame = cv2.cvtColor(avg_frame, cv2.COLOR_BGR2GRAY)
    avg_frame = cv2.GaussianBlur(avg_frame, (21, 21), 0)

    try:
        while True:
            ret, frame = cam.get_frame()
            if ret:
                if detect_motion(frame, avg_frame):
                    print("Motion detected!")
                    cam.start_recording('output.mp4', 10)  # Start recording for 10 seconds
            else:
                print("Failed to read frame")
                
    except KeyboardInterrupt:
        print("Interrupted by user")
    finally:
        cam.stop_immediately()

if __name__ == "__main__":
    main()
