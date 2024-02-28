# Program to capture a frame and split into buffer-sized binary files
# Note [WARN:0] doesn't matter

import cv2
import os
import shutil
import base64

buffer_size = 512

def encode_to_base64(binary_data):
    base64_encoded_data = base64.b64encode(binary_data)
    return base64_encoded_data.decode('ascii')

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
    
    # Convert using base64
    base64_data = (base64.b64encode(capture_bin)).decode("ascii")

    ## CHANGES START HERE
    # Split into buffers
    file_length = len(capture_bin)
   
    # Create new split_capture directory
    os.makedirs("base64_split/", exist_ok=True)
    print("Created base64_split/")

    buffer_number = 0
    while (buffer_number * buffer_size < file_length):
        start_pos = buffer_number * buffer_size
        current_buffer = base64_data[start_pos:start_pos + buffer_size]
        
        # Write the buffer to its own text file
        path = f"base64_split/split_{buffer_number}.txt"
        with open(path, 'w') as buffer_file:
            buffer_file.write(current_buffer)
        
        buffer_number += 1

else:
    print("No image detected")

print("Done.")
