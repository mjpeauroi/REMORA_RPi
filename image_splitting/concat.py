import os
import serial
import time

working_directory = os.path.expanduser('~/Documents/REMORA_RPi/image_splitting')
os.chdir(working_directory)


# Find the number of buffer files generated
directory_path = os.path.expanduser('~/Documents/REMORA_RPi/image_splitting/base64_split/')
if os.path.exists(directory_path):
    # List everything in the directory
    files = os.listdir(directory_path)
    num_buffers = len(files)
    print(f"{num_buffers} buffers found")


for i in range(num_buffers):
    buffer_path = f"base64_split/split_{i}.txt"
    with open(buffer_path, 'r') as buffer_file:
        buffer_data = buffer_file.read()
    with open('concatenated.txt', 'a') as file:
        file.write(buffer_data)

