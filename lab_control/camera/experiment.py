from FLI import FLI
import numpy as np
import sys
sys.path.append('../')
from spectrometer import thr640
import time
import logging
import csv
import xarray as xr

# parameters
EXPOSURE_TIME = 8 # miliseconds
SAVEPATH = ""

# logger
logger = thr640.logger

def write_csv(array):
    with open('some.csv', 'w') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerows(array) # 2次元配列

fli = FLI()
wavelength_controller = thr640.THR640()
"""
main
"""
def take_one_shoot():
    fli = FLI()

    # print information
    logger.info("カメラの温度: {}".format(fli.getTemperature()))
    logger.info("カメラの状態: {}".format(fli.getDeviceStatus()))
    logger.info("カメラモード: {}".format(fli.getCameraModeString(0)))

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

def move_and_shoot(count, exposure_time):
    wavelength_controller.goto(count=count)
    wavelength_controller.waitUntilReady()

    fli.setExposureTime(exposure_time)

    # start exposure
    fli.exposeFrame()
    # exposure終わったらgrab
    array = fli.grabFrame()

    data = xr.DataArray(array, dims=['y', 'x'], coords={'spectrometer_count': count}, 
                        attrs={'temperature': fli.getTemperature(),
                               'device_status': fli.getDeviceStatus(),
                               'camera_mode': fli.getCameraModeString(0),
                               'exposure_time': exposure_time
                               })
    return data

## exposuretime 動かしながら撮影、bin,tempreture固定
def shoot_and_update_exposure():
    output_dir = r'C:\Users\Public\Documents\seminar\exposuretime'

    ## 10ms~10e4msまで調べたい
    bitween = 0.1
    start = 0.9
    for i in range(31):
        start += bitween
        fli.setExposureTime(int(10**start))
        time.sleep(1)

        # start exposure
        fli.exposeFrame()
        # exposure終わったらgrab
        array = fli.grabFrame()

        data = xr.DataArray(array, dims=['y', 'x'], coords={'exposure_time': int(10**start)}, 
                            attrs={'temperature': fli.getTemperature(),
                                'device_status': fli.getDeviceStatus(),
                                'camera_mode': fli.getCameraModeString(0)
                                })
        file=r'\output'+ str(i)+'.nc'
        data.to_netcdf(output_dir + file)
        print(str(i) +'done')
        time.sleep(2)


if __name__ == "__main__":
    shoot_and_update_exposure()
