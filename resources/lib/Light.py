import json
import math
from Logger import Logger
from Constants import HUE_RANGE

class Light:

    hue           = 0
    saturation    = 0
    brightness    = 0
    on            = False
    white         = False
    full_spectrum = False
    logger        = Logger()


    def __init__(self, light_id, name, bridge, settings):
        self.id     = light_id
        self.name   = name
        self.bridge = bridge

        self.get_current_setting()


    def get_current_setting(self):
        data = self.bridge.receive_light_update(self)

        state = data['state']

        self.on         = state['on']
        self.brightness = state['bri']

        if 'sat' in state:
            self.saturation = state['sat']
        if 'hue' in state:
            self.hue = state['hue']
        else:
            self.white = True

        self.full_spectrum = data['modelid'] in ('LST001', 'LST002', 'LLC007')


    def set_light(self, hue, saturation, brightness, duration = 0):
        if not self.white:

            if hue is not None:
                self.hue = hue
            if sat is not None:
                self.saturation = saturation

        if brightness > 0:
            self.on = True
            self.brightness = brightness
        else:
            self.on = False

        self.bridge.send_light_update(self, duration)


    def fade_light_hsv(light, hsv_ratio):
        h, s, v = hsv_ratio.hue(self.full_spectrum)
        hvec = abs(h - self.hue_last) % (HUE_RANGE // 2)
        hvec = hvec / 128.0
        svec = s - self.sat_last
        vvec = v - self.val_last
        distance = math.sqrt(hvec ** 2 + svec ** 2 + vvec ** 2)
        if distance > 0:
            duration = int(3 + 27 * distance / 255)
            # logger.debuglog('distance %s duration %s' % (distance, duration))
            self.set_light(h, s, v, duration)


    # def dim(self):
    #     if self.override_hue:
    #         hue = self.dimmed_hue
        #else:
            #hue = None

        #self.set_light(hue, None, self.dimmed_brightness, self.dim_time)


    #def brighter(self):
        #if self.override_undim_brightness:
            #brightness = self.undim_brightness
        #else:
            #brightness = self.start_setting['bri']

        #if not self.livingwhite:
            #saturation = self.start_setting['sat']

        #if self.override_hue:
            #hue = self.undim_hue
        #else:
            #hue = self.start_setting['hue']
        #else:
            #saturation = None
            #hue        = None

    #self.set_light(hue, sat, bri, self.dim_time)


    #def flash(self):
        #self.dim()
        #time.sleep(self.dim_time / 10)
        #self.brighter()


  #def partial(self):
    #if self.override_paused:
      #brightness = self.paused_brightness
      #if not self.livingwhite:
        #saturation = self.start_setting['sat']

        #if self.override_hue:
          #hue = self.undim_hue
        #else:
          #hue = self.start_setting['hue']
      #else:
        #saturation = None
        #hue = None

      #self.set_light(hue, saturation, brightness, self.dim_time)
    #else:
      ##not enabled for dimming on pause
      #self.brighter_light()
