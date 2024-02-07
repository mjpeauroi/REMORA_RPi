# Code to get temp sensor data

# Reference:
# https://www.circuitbasics.com/raspberry-pi-ds18b20-temperature-sensor-tutorial/

import os
import glob
import time
import serial
from datetime import datetime

bm_tty = '/dev/ttyACM1'
filepath = '~/code/bm_protocol/test_data.txt'
bm_filepath = os.path.expanduser(filepath)

try:
    bm = serial.Serial(bm_tty, 9600)

    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')
    
    base_dir = '/sys/bus/w1/devices/'
    device_folder = glob.glob(base_dir + '28*')[0]
    device_file = device_folder + '/w1_slave'
    
    def read_temp_raw():
        f = open(device_file, 'r')
        lines = f.readlines()
        f.close()
        return lines
    
    def read_temp():
        lines = read_temp_raw()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            temp_f = temp_c * 9.0 / 5.0 + 32.0

            now = datetime.now()
            hour = now.hour
            minute = now.minute
            second = now.second
            timestamp = f"{hour:02d}:{minute:02d}:{second:02d}"

            try:
                if not os.path.exists(bm_filepath):
                    open(bm_filepath, 'w').close()

                with open(bm_filepath, 'a') as file:
                    file.write(f"Time: {timestamp}, Temp: {temp_f}\n")
                    file.flush()  # Ensure data is written immediately
                #bm.write(f"Time: {timestamp}, Temp: {temp_f}")
            except Exception as e:
                print(f"Error writing to {bm_tty}: {str(e)}")

            return temp_c, temp_f
        
    #while True:
    for i in range(10):
        print(read_temp())	
        time.sleep(1)

except Exception as e:
    print(e)
finally:
    bm.close()
    pass
