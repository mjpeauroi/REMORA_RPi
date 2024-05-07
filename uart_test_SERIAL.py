# testing SERIAL method for uart

import serial
import time

# Define the serial port and parameters
#ser = serial.Serial('/dev/ttyAMA0', baudrate=9600, timeout=1, write_timeout=1)
ser = serial.Serial('/dev/ttyS0', baudrate=9600, timeout=1)


try:
    # Open the serial port
    if not ser.is_open:
        ser.open()

    data = "pspspspps\n"
    ser.write(data.encode())
    print(data)
    print(len(data))

    # while True:
    #     time.sleep(0.1)
    #     ser.write((0).to_bytes(1, 'big'))

    #     #ser.write((data % 256).to_bytes(1, 'big'))
    #     print(f"Sent: {data % 256}")
    #     data += 1

finally:
    ser.close()
