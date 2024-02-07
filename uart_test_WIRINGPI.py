# testing WIRINGPI method for uart

import wiringpi
import time

wiringpi.wiringPiSetup()
serial = wiringpi.serialOpen('/dev/ttyAMA0',115200)

t = 0
while True:

    wiringpi.serialPutchar(serial, 0)
    print(f"Sent {t}")
    t = t+1
    time.sleep(1)
