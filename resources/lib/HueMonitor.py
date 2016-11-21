import xbmc
import datetime

class HueMonitor(xbmc.Monitor):

  def __init__(self, *args, **kwargs):
    xbmc.Monitor.__init__(self)


  def onSettingsChanged(self):
    logger.debuglog('running in mode {!s}'.format(hue.settings.mode))
    last = datetime.datetime.now()
    hue.settings.readxml()
    hue.update_settings()
