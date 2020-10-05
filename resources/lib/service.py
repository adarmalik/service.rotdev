import time
import xbmc
import json
import xbmcgui
import xbmcaddon

import struct
import select
import os

def log(txt):
    message = '%s: %s' % ("service.rotdev", txt.encode('ascii', 'ignore'))
    xbmc.log(msg=message, level=xbmc.LOGNOTICE)

def getVolume():
    curVol = -1
    resp = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Application.GetProperties", "params": { "properties": [ "volume"] }, "id": 1}')
    dct = json.loads(resp)
    if (dct.has_key("result")) and (dct["result"].has_key("volume")):
        curVol = dct["result"]["volume"]
    return curVol

def getInputDevice():
    dev = -1
    for fn in os.listdir('/sys/class/input/'):
        if fn.startswith('event'):
            with open('/sys/class/input/' + fn + '/device/name') as f:
                if f.readline(8).startswith('rotary'):
                    dev = int(fn[5:])
                    break
    return dev

class Rotary:    
    def __init__(self):
        self._vol = None
        self._device = None
        
    def __rotate(self, direction):
        vol = getVolume()
        if(direction == -1 and vol > 0):
            xbmc.executebuiltin("SetVolume({}, showVolumeBar)".format(vol-self._vol))
        elif(direction == 1 and vol < 100):
            xbmc.executebuiltin("SetVolume({}, showVolumeBar)".format(vol+self._vol))

    def setup(self):
        log("setup")
        self.stop()

        dev = getInputDevice()
        if dev == -1:
            log("No rotary device found")
            return

        _evdev = "/dev/input/event" + str(dev)

        _this = xbmcaddon.Addon()
        self._vol = int(_this.getSetting("vol_step"))

        log("config: %s %i" % (_evdev, self._vol))
        self._device = open(_evdev, "rb")

    def stop(self):
        log("stop")
        if self._device:
            self._device.close()
            self._device = None

    def read(self):
        if self._device:
            rrdy, wrdy, xrdy = select.select([self._device], [], [], 5);
            if rrdy:
                data = self._device.read(16)
                tmp = struct.unpack('2IHHi',data)
                if tmp[2] == 2:
                    self.__rotate(tmp[4])


class MyMonitor(xbmc.Monitor):
    def __init__(self, rotary):
        xbmc.Monitor.__init__(self)
        self.rotary = rotary

    def onSettingsChanged(self):
        log("onSettingsChanged")
        self.rotary.stop()
        self.rotary.setup()

if __name__ == '__main__':    
    rot = Rotary()
    monitor = MyMonitor(rot)
    rot.setup()
    
    while not monitor.abortRequested():
        rot.read()

    rot.stop()
