import pyfli
import numpy as np
import sys
sys.path.append('../')
from spectrometer import thr640
import os
import time
import logging

## parameters
DEVICE = 'camera'
INTERFACE = 'usb'
FRAME_TYPE = "normal" ## {'normal', 'dark', 'flood', 'flush'}
handle = None
EXPOSURE_TIME = 50

# """
# configure logging
# """
# logger = logging.getLogger('Logging')
# logger.setLevel(10)
# formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
# sh = logging.StreamHandler()
# sh.setFormatter(formatter)
# logger.addHandler(sh)
logger = thr640.logger

"""
configure functions
"""
## mode: {0,1}, return value = xxKHZ
def getCameraModeString(mode:int):
    return pyfli.getCameraModeString(handle,mode)

## Get the remaining camera exposure time. exposure time given in milliseconds
def getExposureStatus():
    return pyfli.getExposureStatus(handle)

def getDeviceStatus():
    return pyfli.getDeviceStatus(handle)

def getTemperature():
    return pyfli.getTemperature(handle)

def grabFrame():
    return pyfli.grabFrame(handle)

## open shutter and expose frame. exposes a frame according to the settings (image area,
## exposure time, bit depth, etc.). exposure time should be assigned before.
## This function returns after the exposure has started
def exposeFrame():
    pyfli.exposeFrame(handle)

def endExposure():
    pyfli.endExposure(handle)

## you should give exposure time in milliseconds
def setExposureTime(time):
    pyfli.setExposureTime(handle,time)

def setTemperature():
    pyfli.setTemperature(handle)

def FLIClose():
    pyfli.FLIClose(handle)

"""
main
"""
def main():
    fli_list = pyfli.FLIList(INTERFACE,DEVICE)
    if not fli_list:
        Exception("No Device can be Found")
    
    DEVICE_PATH, DEVICE_NAME = fli_list[0]
    global handle
    handle = pyfli.FLIOpen(DEVICE_PATH,INTERFACE,DEVICE)

    ## information
    logger.info("カメラの温度: {}".format(getTemperature()))
    logger.info("カメラの状態: {}".format(getDeviceStatus()))
    logger.info("カメラモード: {}".format(getCameraModeString(0)))

    setExposureTime(EXPOSURE_TIME)
    exposeFrame()

    while True:
        if getExposureStatus() == 10:
            break

    array = grabFrame()
    print(array)
    FLIClose()

if __name__ == "__main__":
    main()