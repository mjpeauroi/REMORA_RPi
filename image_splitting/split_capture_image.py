import cv2
import os
import shutil


# Initialize the camera module and take a picture
cam = cv2.VideoCapture(0)
result, image = cam.read()
cam.release()  # Release the camera

if result:
    # cleanup image and buffers from previous runs
    if os.path.exists("capture.jpg"):
        os.remove("capture.jpg")
        print("Deleted capture.jpg")
    if os.path.exists("split_capture"):
        shutil.rmtree("split_capture")
        print("Deleted all files in split_capture")

    cv2.imwrite("capture.jpg", image)
    
    # Read the image as binary data
    with open("capture.jpg", 'rb') as image_file:
        capture_bin = image_file.read()
    
    # Split into buffers
    buffer_size = 2048
    file_length = len(capture_bin)
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
