import cv2
import os

# inialize the camera module and take a pic
cam = cv2.VideoCapture(0) 
result, image = cam.read() 

if result: 
	cv2.imwrite("capture.jpg", image) 
else: 
	print("No image detected. Please! try again") 

# # find the dimensions
# height, width, channels = image.shape
# print("dimensions: ", height, ",", width, ",", channels)
# # find the file size
# file_size = os.stat('capture.jpg')
# print("file size: ", file_size.st_size, "bytes")

# Read the image as binary data
with open('capture.jpg', 'rb') as image_file:
	capture_bin = image_file.read()
	file_length = len(capture_bin)

# Save this binary data to a .txt file
with open('capture_bin.txt', 'wb') as txt_file:
    txt_file.write(capture_bin)

# split into individual buffers
buffer_size = 2048
buffer_number = 0
while (buffer_number * (buffer_size-1) < file_length):

	with open("capture_bin.txt", 'rb') as binary_file:
        # Calculate the starting position for this buffer
		start_pos = buffer_number * buffer_size
		binary_file.seek(start_pos)
        # read either buffer_size or the remaining amount of binary_file
		read_size = min(buffer_size - 1, file_length - start_pos)
		print(read_size)
		current_buffer = binary_file.read(read_size)

	# write the buffer to its own file
	path = "split_capture/split_capture_" + str(buffer_number) + ".txt"
	with open(path, 'wb') as txt_file:
		txt_file.write(current_buffer)
		txt_file.write('\n'.encode())

	buffer_number += 1