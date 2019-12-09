import pyfli
import numpy as np


## parameters
DEVICE_PATH = ''
DEVICE = 'camera'
INTERFACE = 'usb'
DEVICE_NAME = ""
def main():
    fli_list = pyfli.FLIList(INTERFACE,DEVICE)

    if not fli_list:
        Exception("No Device can be Found")
    
    DEVICE_PATH, DEVICE_NAME = fli_list[0]
    handle = pyfli.FLIOpen(DEVICE_PATH,INTERFACE,DEVICE)


    print("カメラの温度: {}".format(pyfli.getTemperature(handle)))
    print("カメラの状態: {}".format(pyfli.getDeviceStatus(handle)))
    # a = pyfli.controlShutter(handle,'close',None)
    pyfli.setFrameType(handle,'normal')
    # print(pyfli.getPixelSize(handle))
    pyfli.setExposureTime(handle,10)

    print(pyfli.getCameraModeString(handle,0))
    print(pyfli.getArrayArea(handle))
    print(pyfli.getVisibleArea(handle))
    print(pyfli.getExposureStatus(handle))

    pyfli.exposeFrame(handle)
    print(pyfli.getExposureStatus(handle))

    array = pyfli.grabFrame(handle)
    print(array)
    print(np.count_nonzero(array))

    pyfli.FLIClose(handle)

if __name__ == "__main__":
    main()