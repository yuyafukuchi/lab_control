from FLI import FLI
import numpy as np
import sys
sys.path.append('../')
from spectrometer import thr640
import time
import logging
import csv
import xarray as xr

# logger
logger = thr640.logger


# global instance
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
撮影して回折格子動かす
"""
def move_and_shoot(count,exposure_time):
    wavelength_controller.goto(count=count)
    wavelength_controller.waitUntilReady()

    # start exposure
    fli.exposeFrame()
    # exposure終わったらgrab
    array = fli.grabFrame()
    time.sleep(.5)

    data = xr.DataArray(array, dims=['y', 'x'], coords={'spectrometer_count': count}, 
                        attrs={'temperature': fli.getTemperature(),
                               'device_status': fli.getDeviceStatus(),
                               'camera_mode': fli.getCameraModeString(0),
                               'exposure_time': exposure_time
                               })
    return data

"""
撮影して回折格子動かす(早いver)
"""
def fast_move_and_shoot(count,exposure_time):
    wavelength_controller.goto(count=count)

    # start exposure
    fli.exposeFrame()
    # exposure終わったらgrab
    array = fli.grabFrame()
    time.sleep(.5)

    data = xr.DataArray(array, dims=['y', 'x'], coords={'spectrometer_count': count}, 
                        attrs={'temperature': fli.getTemperature(),
                               'device_status': fli.getDeviceStatus(),
                               'camera_mode': fli.getCameraModeString(0),
                               'exposure_time': exposure_time
                               })
    return data

"""
撮影して回折格子動かすを繰り返す
"""
def repeat_move_and_shoot(start_count,count_interval,taken_count,exposuretime,output_dir):
    fli.setExposureTime(exposuretime)

    for i in range(taken_count):
        data = move_and_shoot(count=start_count,exposure_time=exposuretime)
        file=r'\output'+ str(i)+'.nc'
        data.to_netcdf(output_dir + file)
        start_count+=count_interval

"""
シャッターを開けて撮影、閉じて撮影して回折格子動かすを繰り返す
"""
def repeat_move_and_shoot_with_shutter_control(start_count,count_interval,taken_count,exposuretime,output_dir,output_dir_with_shutter_close):
    fli.setExposureTime(exposuretime)
    for i in range(taken_count):
        # -------shutterを開けて撮影---------
        fli.setFrameType('normal')
        time.sleep(1)
        ## move
        wavelength_controller.goto(count=start_count)
        time.sleep(3)
        # start exposure
        fli.exposeFrame()
        array = fli.grabFrame()
        time.sleep(1)

        data = xr.DataArray(array, dims=['y', 'x'], coords={'spectrometer_count': start_count}, 
                            attrs={'temperature': fli.getTemperature(),
                                'device_status': fli.getDeviceStatus(),
                                'exposure_time': exposuretime,
                                'frame_type': 'normal'
                                })
        file=r'\output'+ str(i)+'.nc'
        data.to_netcdf(output_dir + file)

        time.sleep(3)

        # -------shutterを閉じて撮影---------
        fli.setFrameType('dark')
        time.sleep(1)

        fli.exposeFrame()
        array = fli.grabFrame()
        time.sleep(1)

        data = xr.DataArray(array, dims=['y', 'x'], coords={'spectrometer_count': start_count}, 
                            attrs={'temperature': fli.getTemperature(),
                                'device_status': fli.getDeviceStatus(),
                                'exposure_time': exposuretime,
                                'frame_type': 'dark'
                                })
        file=r'\output'+ str(i)+'_with_shutter_close'+'.nc'
        data.to_netcdf(output_dir_with_shutter_close + file)

        ## start_countあげて次のループへ
        start_count+=count_interval
        time.sleep(.5)


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
        time.sleep(.1)
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
    output_dir = r'C:\Users\Public\Documents\seminar\exposuretime_with_shutter_control\no_shutter'
    output_dir2 = r'C:\Users\Public\Documents\seminar\exposuretime_with_shutter_control\shutter'

    repeat_move_and_shoot_with_shutter_control(start_count=-40000,count_interval=4000,taken_count=50,exposuretime=1000,output_dir=output_dir,output_dir_with_shutter_close=output_dir2)
