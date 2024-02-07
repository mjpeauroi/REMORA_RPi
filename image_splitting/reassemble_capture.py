import os

# Adjust working directory
working_directory = os.path.expanduser('~/Documents/REMORA_RPi/image_splitting')
os.chdir(working_directory)

# Cleanup old reassembled_capture
if os.path.exists("reassembled_capture.jpg"):
    os.remove("reassembled_capture.jpg")
    print("Deleted reassembled_capture.jpg")

# Find the number of buffer files generated
directory_path = os.path.expanduser('~/Documents/REMORA_RPi/image_splitting/split_capture/')
if os.path.exists(directory_path):
    # List everything in the directory
    files = os.listdir(directory_path)
    num_buffers = len(files)
    print(f"{num_buffers} buffers found")

# Reassemble the binary data from the split files
reassembled_data = bytearray()
for i in range(num_buffers):
    buffer_path = f"split_capture/split_capture_{i}.bin"
    with open(buffer_path, 'rb') as buffer_file:
        reassembled_data += buffer_file.read()

# Save the reassembled data back to a JPEG file
with open("reassembled_capture.jpg", 'wb') as output_file:
    output_file.write(reassembled_data)
print("Created reassembled_capture.jpg")
