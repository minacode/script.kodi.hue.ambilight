import xbmc
import xbmcgui
import xbmcaddon
import json
import time
import sys
import colorsys
import os
import datetime
import math
from typing import Callable, List, Tuple

__addon__      = xbmcaddon.Addon()
__cwd__        = __addon__.getAddonInfo('path')
__resource__   = xbmc.translatePath(os.path.join(__cwd__, 'resources', 'lib'))

sys.path.append(__resource__)

from Settings  import *
from tools     import *
from MyPlayer  import MyPlayer
from MyMonitor import MyMonitor
from HSVRatio  import HSVRatio

try:
  import requests
except ImportError:
  xbmc.log('ERROR: Could not locate required library requests')
  notify('Kodi Hue', 'ERROR: Could not import Python requests')

xbmc.log('Kodi Hue service started, version: {!s}'.format( get_version() ))

capture = xbmc.RenderCapture()
fmt     = capture.getImageFormat()
# BGRA or RGBA
# xbmc.log('Hue Capture Image format: %s' % fmt)
fmtRGBA = fmt == 'RGBA'


monitor = MyMonitor()


def run() -> None:
  player = None
  last = datetime.datetime.now()

  while not xbmc.abortRequested:
    
    if hue.settings.mode == 1: # theatre mode
      if player is None:
        logger.debuglog('creating instance of player')
        player = MyPlayer()
      xbmc.sleep(500)
    if hue.settings.mode == 0: # ambilight mode
      if hue.settings.ambilight_dim and hue.dim_group is None:
        logger.debuglog('creating group to dim')
        tmp = hue.settings
        tmp.group_id = tmp.ambilight_dim_group
        hue.dim_group = Group(tmp)
      
      if player is None:
        player = MyPlayer()
      else:
        xbmc.sleep(100)

      capture.waitForCaptureStateChangeEvent(1000 / 60)
      if capture.getCaptureState() == xbmc.CAPTURE_STATE_DONE:
        if player.playingvideo:
          screen = Screenshot(capture.getImage(), capture.getWidth(), capture.getHeight())
          hsvRatios = screen.spectrum_hsv(screen.pixels, screen.capture_width, screen.capture_height)
          if hue.settings.light == 0:
            fade_light_hsv(hue.light, hsvRatios[0])
          else:
            fade_light_hsv(hue.light[0], hsvRatios[0])
            if hue.settings.light > 1:
              xbmc.sleep(4)
              fade_light_hsv(hue.light[1], hsvRatios[1])
            if hue.settings.light > 2:
              xbmc.sleep(4)
              fade_light_hsv(hue.light[2], hsvRatios[2])


def fade_light_hsv(light: Light, hsvRatio: HSVRatio) -> None:
        
    fullSpectrum = light.fullSpectrum
    h, s, v = hsvRatio.hue(fullSpectrum)
    hvec = abs(h - light.hueLast) % int(65535 / 2)
    hvec = float(hvec / 128.0)
    svec = s - light.satLast
    vvec = v - light.valLast
    distance = math.sqrt(hvec **2 + svec **2 + vvec **2)
    if distance > 0:
        duration = int(3 + 27 * distance / 255)
        # logger.debuglog('distance %s duration %s' % (distance, duration))
        light.set_light(h, s, v, duration)


def state_changed(state: str, duration: int) -> None:
    
    logger.debuglog('state changed to: {!s}'.format(state))
      
    # detect pause for refresh change
    pauseafterrefreshchange = 0
    response = json.loads(xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.GetSettingValue", "params":{"setting":"videoplayer.pauseafterrefreshchange"},"id":1}'))
      
    # logger.debuglog(isinstance(response, dict))
     
    if 'result' in response and 'value' in response['result']:
        pauseafterrefreshchange = int(response['result']['value'])
    
    if duration < 300 and hue.settings.misc_disableshort:
        logger.debuglog('add-on disabled for short movies')
        return
    
    if state == 'started':
        logger.debuglog('retrieving current setting before starting')
        
    if hue.settings.light == 0:
          hue.light.get_current_setting()
    else:
        hue.light[0].get_current_setting()
        if hue.settings.light > 1:
            xbmc.sleep(1)
            hue.light[1].get_current_setting()
        if hue.settings.light > 2:
            xbmc.sleep(1)
            hue.light[2].get_current_setting()
    
    if hue.settings.mode == 0: # ambilight mode
        # start capture when playback starts
        capture_width = 32 # 100
        capture_height = int(capture_width / capture.getAspectRatio())
        logger.debuglog('capture %s x %s' % (capture_width, capture_height))
        capture.capture(capture_width, capture_height, xbmc.CAPTURE_FLAG_CONTINUOUS)
    
    if (state == 'started' and pauseafterrefreshchange == 0) or state == 'resumed':
        if hue.settings.mode == 0 and hue.settings.ambilight_dim: # only if a complete group
            logger.debuglog('dimming group for ambilight')
            hue.dim_group.dim_light()
        else:
            logger.debuglog('dimming lights')
            hue.dim_lights()
    elif state == 'paused' and hue.last_state == 'dimmed':
        # only if its coming from being off
        if hue.settings.mode == 0 and hue.settings.ambilight_dim:
            # Be persistent in restoring the lights 
            # (prevent from being overwritten by an ambilight update)
            for i in range(0, 3):
                logger.debuglog('partial lights')
                hue.dim_group.partial_lights()
                time.sleep(1)
        else:
            hue.partial_lights()
    elif state == 'stopped':
        if hue.settings.mode == 0 and hue.settings.ambilight_dim:
            # Be persistent in restoring the lights 
            # (prevent from being overwritten by an ambilight update)
            for i in range(0, 3):
                logger.debuglog('brighter lights')
                hue.dim_group.brighter_light()
                time.sleep(1)
        else:
            hue.brighter_lights()
    
    
if __name__ == '__main__':
    settings = settings()
    logger = Logger()
    if settings.debug:
        logger.debug()
  
    args = None
    if len(sys.argv) == 2:
        args = sys.argv[1]
    hue = Hue(settings, args)
    while not hue.connected:
        logger.debuglog('not connected')
        time.sleep(1)
    run()
