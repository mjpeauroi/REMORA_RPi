# Program to capture a frame and split into buffer-sized binary files
# Note [WARN:0] doesn't matter

import cv2
import os
import shutil
import base64

buffer_size = 1024
compression_quality = 10

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
    if os.path.exists("base64_splits/"):
        shutil.rmtree("base64_splits/")
        print("Deleted base64_splits/")
    
    # # Read the image as binary data
    # cv2.imwrite("capture.jpg", image)

    # Get the index label for this image
    directory_path = os.path.expanduser('~/Documents/REMORA_RPi/image_splitting/capture_archive/')
    if os.path.exists(directory_path):
        # List everything in the directory
        files = os.listdir(directory_path)
        this_capture_index = len(files)

    height, width = image.shape[:2]
    top_left_quarter = image[:height//2, :width//2]

    # Compress and save the image
    image_path = os.path.expanduser(f'~/Documents/REMORA_RPi/image_splitting/capture_archive/capture_{this_capture_index}.jpg')
    cv2.imwrite(image_path, top_left_quarter, [int(cv2.IMWRITE_JPEG_QUALITY), compression_quality])

    print(f"Created capture_{this_capture_index}.jpg")
    with open(image_path, 'rb') as image_file:
        capture_bin = image_file.read()

    # Convert using base64
    base64_data = (base64.b64encode(capture_bin)).decode("ascii")

    ## CHANGES START HERE
    # Split into buffers
    file_length = len(capture_bin)
   
    # Create new split_capture directory
    os.makedirs("base64_splits/", exist_ok=True)
    print("Created base64_splits/")

    buffer_number = 0
    while (buffer_number * buffer_size < file_length):
        start_pos = buffer_number * buffer_size
        current_buffer = base64_data[start_pos:start_pos + buffer_size]
        
        # Write the buffer to its own text file
        path = f"base64_splits/split_{buffer_number}.txt"
        with open(path, 'w') as buffer_file:
            buffer_file.write(current_buffer)
        
        buffer_number += 1
    print(f"Saved {buffer_number} buffer txt files.")

else:
    print("No image detected")

print("Done.")
