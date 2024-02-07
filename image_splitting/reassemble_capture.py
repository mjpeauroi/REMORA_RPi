import os
import shutil

num_buffers = 132

# if os.path.exists("/split_capture"):
#     shutil.rmtree("/split_capture")
# os.makedirs("/split_capture")

# Reassemble the binary data from the split files
reassembled_data = bytearray()
for i in range(num_buffers):
    buffer_path = f"split_capture/split_capture_{i}.bin"
    with open(buffer_path, 'rb') as buffer_file:
        reassembled_data += buffer_file.read()

# Save the reassembled data back to a JPEG file
with open("reassembled_capture.jpg", 'wb') as output_file:
    output_file.write(reassembled_data)
