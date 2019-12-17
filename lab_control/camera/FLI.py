import pyfli

class FLI: 
    def __init__(self):
        self.DEVICE = 'camera'
        self.INTERFACE = 'usb'
        self.FRAME_TYPE = "normal" # {'normal', 'dark', 'flood', 'flush'}
        self.handle = None
        
        self._initialize()

    def _initialize(self):
        fli_list = pyfli.FLIList(self.INTERFACE,self.DEVICE)
        if not fli_list:
            Exception("No device can be found")
        
        DEVICE_PATH, DEVICE_NAME = fli_list[0]
        self.handle = self.FLIOpen(DEVICE_PATH,self.INTERFACE,self.DEVICE)

    # mode: {0,1}, return value = xxKHZ
    def getCameraModeString(self,mode: int):
        return pyfli.getCameraModeString(self.handle,mode)

    # Get the remaining camera exposure time. exposure time given in milliseconds
    def getExposureStatus(self):
        return pyfli.getExposureStatus(self.handle)

    def getDeviceStatus(self):
        return pyfli.getDeviceStatus(self.handle)

    def getTemperature(self):
        return pyfli.getTemperature(self.handle)

    def grabFrame(self):
        return pyfli.grabFrame(self.handle)
    
    def setFrameType(self,ftype):
        """
        Parameters
        ----------
        dev : int
            Device handle.
        ftype : {'normal', 'dark', 'flood', 'flush'}
            The frame type. The last two are associated with the RBI and
            are guesses as they aren't documented.
            I guess 'dark' type is taking photo without opening shutter.
        """
        pyfli.setFrameType(self.handle,ftype)

    def setHBin(self, hbin):
        """
        Parameters
        ----------
        hbin : int
            Bin horizontal dimension in pixels. The valid range is 1..16.
        """
        pyfli.setHBin(self.handle,hbin)


    def setVBin(self, vbin):
        """
        Parameters
        ----------
        vbin : int
            Bin vertical dimension in pixels. The valid range is 1..16.
        """
        pyfli.setVBin(self.handle,vbin)



    # open shutter and expose frame. exposes a frame according to the settings (image area,
    # exposure time, bit depth, etc.). exposure time should be assigned before.
    # This function returns after the exposure has started
    def exposeFrame(self):
        pyfli.exposeFrame(self.handle)

    def cancelExposure(self):
        pyfli.cancelExposure(self.handle)

    # you should give exposure time in milliseconds
    def setExposureTime(self,time):
        pyfli.setExposureTime(self.handle,time)

    def setTemperature(self,t):
        pyfli.setTemperature(self.handle,t)

    def FLIOpen(self,device_path,interface,device):
        return pyfli.FLIOpen(device_path,interface,device)

    def FLIClose(self):
        pyfli.FLIClose(self.handle)

    def unlockDevice(self):
        pyfli.unlockDevice(self.handle)
