import pyfli
import numpy as np
import sys
sys.path.append('../')
from spectrometer import thr640
import time
import logging
import csv

# parameters
DEVICE = 'camera'
INTERFACE = 'usb'
FRAME_TYPE = "normal" # {'normal', 'dark', 'flood', 'flush'}
handle = None
EXPOSURE_TIME = 8 # miliseconds
SAVEPATH = ""

# logger
logger = thr640.logger

"""
configure functions
"""
# mode: {0,1}, return value = xxKHZ
def getCameraModeString(mode:int):
    return pyfli.getCameraModeString(handle,mode)

# Get the remaining camera exposure time. exposure time given in milliseconds
def getExposureStatus():
    return pyfli.getExposureStatus(handle)

def getDeviceStatus():
    return pyfli.getDeviceStatus(handle)

def getTemperature():
    return pyfli.getTemperature(handle)

def grabFrame():
    return pyfli.grabFrame(handle)

# open shutter and expose frame. exposes a frame according to the settings (image area,
# exposure time, bit depth, etc.). exposure time should be assigned before.
# This function returns after the exposure has started
def exposeFrame():
    pyfli.exposeFrame(handle)

def cancelExposure():
    pyfli.cancelExposure(handle)

# you should give exposure time in milliseconds
def setExposureTime(time):
    pyfli.setExposureTime(handle,time)

def setTemperature():
    pyfli.setTemperature(handle)

def FLIOpen(device_path,interface,device):
    return pyfli.FLIOpen(device_path,interface,device)

def FLIClose():
    pyfli.FLIClose(handle)

def unlockDevice():
    pyfli.unlockDevice(handle)


def write_csv(array):
    with open('some.csv', 'w') as f:
        writer = csv.writer(f, lineterminator='\n')
        # writer.writerow(list)     # list（1次元配列）の場合
        writer.writerows(array) # 2次元配列

"""
main
"""
def main():
    controller = thr640.THR640()
    # get camera information
    fli_list = pyfli.FLIList(INTERFACE,DEVICE)
    if not fli_list:
        Exception("No device can be found")
    
    DEVICE_PATH, DEVICE_NAME = fli_list[0]
    global handle
    handle = FLIOpen(DEVICE_PATH,INTERFACE,DEVICE)

    # print information
    logger.info("カメラの温度: {}".format(getTemperature()))
    logger.info("カメラの状態: {}".format(getDeviceStatus()))
    logger.info("カメラモード: {}".format(getCameraModeString(0)))

    controller.goto(count=-97000)
    controller.waitUntilReady()

    setExposureTime(EXPOSURE_TIME)

    # start exposure
    exposeFrame()

    # exposure終わったらgrab
    array = grabFrame()

    ## TODO: 出力
    print(array)
    FLIClose()

def continuousShooting(startCoordinate: int,endCoordinate: int, coordinateInterval: int, exposureTimes: "List[int]"):
    '''
    ==========
    Parameters
    ==========

    startCoordinate: 最初の回折格子の座標
    coordinateInterval: 撮影が終わったらこの値の分だけ座標更新。正の数
    endCoordinate: 回折格子の座標がこの値を超えたら終了。start<endで指定
    exposureTimes: 露光時間のリスト。一つの座標につきexposureTimesの要素数回撮影が行われる.
    '''
    controller = thr640.THR640()

    # get camera information
    fli_list = pyfli.FLIList(INTERFACE,DEVICE)
    if not fli_list:
        Exception("No device can be found")
    
    DEVICE_PATH, DEVICE_NAME = fli_list[0]
    global handle
    handle = FLIOpen(DEVICE_PATH,INTERFACE,DEVICE)

    currentCoordinate = startCoordinate

    logger.info("start operating...")
    while currentCoordinate < endCoordinate:
        logger.info("Move to {}".format(currentCoordinate))
        controller.goto(count=currentCoordinate)
        controller.waitUntilReady()
        setExposureTime(EXPOSURE_TIME)
        exposeFrame()
        # TODO: 出力
        array = grabFrame()
        print(array)
        currentCoordinate+=coordinateInterval

    logger.info("Successfully finish operating!!!")
    FLIClose()


if __name__ == "__main__":
    main()