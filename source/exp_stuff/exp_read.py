# coding: utf-8
import os
import time
import busio
import digitalio
import board
import math
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D22)

# create the mcp object
mcp = MCP.MCP3008(spi, cs)


# create an analog input channel on pin 0
chan0 = AnalogIn(mcp, MCP.P0)


def get_exp_value():
    return math.floor(max(min(((1.024*chan0.value/512) - 2), 127), 0))

'''
print("Starting 2 test...")
try:
    while True:
        print(get_exp_value())
        time.sleep(0.2)
        
finally:
    print('Done.')
'''