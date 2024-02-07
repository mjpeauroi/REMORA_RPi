# Program to capture a frame and split into buffer-sized binary files
# Note [WARN:0] doesn't matter

import cv2
import os
import shutil

# Adjust working directory
working_directory = os.path.expanduser('~/Documents/REMORA_RPi/image_splitting')
os.chdir(working_directory)

# Initialize the camera module and take a picture
cam = cv2.VideoCapture(0)
result, image = cam.read()
print("Image captured")
cam.release()  # Release the camera

if result:

    # cleanup image and buffers from previous runs
    if os.path.exists("capture.jpg"):
        os.remove("capture.jpg")
        print("Deleted capture.jpg")
    if os.path.exists("split_capture/"):
        shutil.rmtree("split_capture/")
        print("Deleted split_capture/")
    
    # Read the image as binary data
    cv2.imwrite("capture.jpg", image)
    print("Created capture.jpg")
    with open("capture.jpg", 'rb') as image_file:
        capture_bin = image_file.read()
    
    # Split into buffers
    buffer_size = 2048
    file_length = len(capture_bin)
   
    # Create new split_capture directory
    os.makedirs("split_capture/", exist_ok=True)
    print("Created split_capture/")

    buffer_number = 0
    while (buffer_number * buffer_size < file_length):
        # Calculate the starting position for this buffer
        start_pos = buffer_number * buffer_size
        # Determine the chunk of binary data
        current_buffer = capture_bin[start_pos:start_pos + buffer_size]
        
        # Write the buffer to its own file
        path = f"split_capture/split_capture_{buffer_number}.bin"
        with open(path, 'wb') as buffer_file:
            buffer_file.write(current_buffer)
        
        buffer_number += 1
else:
    print("No image detected")

print("Done.")
