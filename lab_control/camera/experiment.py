from FLI import FLI
import numpy as np
import sys
sys.path.append('../')
from spectrometer import thr640
import time
import logging
import csv

# parameters
EXPOSURE_TIME = 8 # miliseconds
SAVEPATH = ""

# logger
logger = thr640.logger

def write_csv(array):
    with open('some.csv', 'w') as f:
        writer = csv.writer(f, lineterminator='\n')
        # writer.writerow(list)     # list（1次元配列）の場合
        writer.writerows(array) # 2次元配列

"""
main
"""
def main():
    fli = FLI()

    # print information
    logger.info("カメラの温度: {}".format(fli.getTemperature()))
    logger.info("カメラの状態: {}".format(fli.getDeviceStatus()))
    logger.info("カメラモード: {}".format(fli.getCameraModeString(0)))

    # controller = thr640.THR640()
    # controller.goto(count=-97000)
    # controller.waitUntilReady()

    fli.setExposureTime(EXPOSURE_TIME)

    # start exposure
    fli.exposeFrame()

    # exposure終わったらgrab
    array = fli.grabFrame()

    ## TODO: 出力
    print(array)

"""
撮影して回折格子動かすを繰り返す
"""
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