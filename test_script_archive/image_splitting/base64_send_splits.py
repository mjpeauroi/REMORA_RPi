import os
import serial
import time

def send():
    working_directory = os.path.expanduser('~/Documents/REMORA_RPi/image_splitting')
    os.chdir(working_directory)

    # Find the number of buffer files generated
    directory_path = os.path.expanduser('~/Documents/REMORA_RPi/image_splitting/base64_splits/')
    if os.path.exists(directory_path):
        # List everything in the directory
        files = os.listdir(directory_path)
        num_buffers = len(files)
        print(f"{num_buffers} buffers found")

    # Get the index label for this image
    directory_path = os.path.expanduser('~/Documents/REMORA_RPi/image_splitting/capture_archive/')
    if os.path.exists(directory_path):
        # List everything in the directory
        files = os.listdir(directory_path)
        this_capture_index = len(files) - 1

    ser = serial.Serial('/dev/ttyS0', baudrate=9600, timeout=1)
    #ser = serial.Serial('/dev/ttyAMA0', baudrate=9600, timeout=1)

    try:
        # Open the serial port
        if not ser.is_open:
            ser.open()
        buffer_to_send = f"<START IMG {this_capture_index}> length: {num_buffers}\n"
        ser.write(buffer_to_send.encode('ascii'))
        print(f'Sent {buffer_to_send}')
        time.sleep(5) # wait to ensure the start tag sends fully

        for i in range(num_buffers):
            buffer_path = f"base64_splits/split_{i}.txt"
            with open(buffer_path, 'r') as buffer_file:
                buffer_data = buffer_file.read()
            buffer_to_send = f"<I{i}>" + buffer_data + '\n'
            ser.write(buffer_to_send.encode('ascii'))
            print(f'Sent buffer {i} of {num_buffers}')
            time.sleep(1)

        time.sleep(4) # wait to ensure all send before the end tag
        buffer_to_send = f"<END IMG {this_capture_index}>\n"
        ser.write(buffer_to_send.encode('ascii'))
        print(f'Sent {buffer_to_send}')

    finally:
        ser.close()

if __name__ == "__main__":
    send()