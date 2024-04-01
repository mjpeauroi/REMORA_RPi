import cv2
import time

# Initialize video capture
cam = cv2.VideoCapture(0)

# Check if the webcam is opened correctly
if not cam.isOpened():
    raise IOError("Cannot open webcam")

# Get default video capture frame rate
fps = cam.get(cv2.CAP_PROP_FPS)

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('test_vid.mp4', fourcc, fps, (int(cam.get(3)), int(cam.get(4))))

start_time = time.time()
while True:
    ret, frame = cam.read()
    if not ret:
        print("Failed to grab frame")
        break
    # Write the frame to the video file
    out.write(frame)

    # Break the loop after 6 seconds
    if time.time() - start_time > 6:
        break

# Release everything
cam.release()
out.release()
cv2.destroyAllWindows()

print("6-second video captured")
