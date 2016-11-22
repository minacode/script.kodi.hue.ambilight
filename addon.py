import xbmc
import xbmcaddon
import os
import sys
import datetime
import requests

ADDON = xbmcaddon.Addon()
ADDON_PATH = ADDON.getAddonInfo('path')
LIB_PATH = xbmc.translatePath(os.path.join(ADDON_PATH, 'resources', 'lib'))

sys.path.append(LIB_PATH)

from Logger import Logger
from Settings import Settings
from Hue import Hue
from HuePlayer import HuePlayer
from HueMonitor import HueMonitor
from HSVRatio import HSVRatio
from tools import *
from Constants import MODE_THEATRE, MODE_AMBILIGHT

def run(hue, monitor, player, settings):
    last = datetime.datetime.now()

    while not xbmc.abortRequested:

        if settings['mode'] == MODE_THEATRE:
            pass # ? thought something happened here
        elif settings['mode'] == MODE_AMBILIGHT:
            capture = xbmc.RenderCapture()
            fmt = capture.getImageFormat()
            # BGRA or RGBA
            # xbmc.log('Hue Capture Image format: %s' % fmt)
            fmtRGBA = fmt == 'RGBA'

            # TODO
            if settings['ambilight']['dim'] and settings['dim_group'] is None:
                logger.debuglog('creating group to dim')
                tmp = settings
                tmp.data['group_id'] = tmp.data['ambilight']['dim_group']
                hue.dim_group = Group(tmp)

            capture.waitForCaptureStateChangeEvent(1000 / 60)
            if capture.getCaptureState() == xbmc.CAPTURE_STATE_DONE:
                if player.playing_video:
                    screenshot = Screenshot(capture.getImage(),
                        capture.getWidth(), capture.getHeight())
                    hsv_ratios = screenshot.spectrum_hsv(screenshot.pixels,
                        screenshot.capture_width, screenshot.capture_height)

                    i = 0
                    for light in hue.lights:
                        fade_light_hsv(light, )

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


def state_changed(state, duration):

    logger.debuglog('state changed to: {!s}'.format(state))

    # detect pause for refresh change
    pauseafterrefreshchange = 0
    response = json.loads(xbmc.executeJSONRPC(
        '{"jsonrpc":"2.0","method":"Settings.GetSettingValue", "params":{"setting":"videoplayer.pauseafterrefreshchange"},"id":1}'))

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

    if hue.settings.mode == 0:  # ambilight mode
        # start capture when playback starts
        capture_width = 32  # 100
        capture_height = int(capture_width / capture.getAspectRatio())
        logger.debuglog('capture %s x %s' % (capture_width, capture_height))
        capture.capture(capture_width, capture_height,
                        xbmc.CAPTURE_FLAG_CONTINUOUS)

    if (state == 'started' and pauseafterrefreshchange == 0) or state == 'resumed':
        if hue.settings.mode == 0 and hue.settings.ambilight_dim:  # only if a complete group
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


def discover_lights(settings, hue):
    settings.update_lights(hue.get_lights(), [])


if __name__ == '__main__':
    xbmc.log('Kodi Hue service started, version: {!s}'.format(get_version()))

    # kodi objects
    monitor = HueMonitor()
    player  = HuePlayer()

    settings = Settings(ADDON, ADDON_PATH)
    logger = Logger()

    args = dict(arg.split('=') for arg in sys.argv.split('&'))

    discover = False
    if 'action' in args.keys():
        discover = args['action'] == 'discover_bridge'
    hue = Hue(settings, discover)

    if 'action' in args.keys() and args['action'] == 'discover_lights':
        discover_lights(settings, hue)


    # dont like this part
    while not hue.connected:
        logger.debuglog('not connected')
        time.sleep(1)
    run(hue, monitor, player, settings)
