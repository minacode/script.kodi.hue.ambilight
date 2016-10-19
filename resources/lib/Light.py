# TODO: deleted some start-stuff.. need to look, what it does

import json
from Logger import Logger

class Light:
    
    start_setting = {}
    group         = False
    livingwhite   = False
    fullSpectrum  = False


    def __init__(self, light_id, bridge, settings):
        self.logger = Logger()

        self.id                 = light_id # type = str
        self.bridge             = bridge
        self.dim_time           = settings.dim_time
        self.override_hue       = settings.override_hue
        self.dimmed_bri         = settings.dimmed_bri
        self.dimmed_hue         = settings.dimmed_hue
        self.override_paused    = settings.override_paused
        self.paused_bri         = settings.paused_bri
        self.undim_bri          = settings.undim_bri
        self.undim_hue          = settings.undim_hue
        self.override_undim_bri = settings.override_undim_bri
        self.last = {
            'hue': 0, 
            'sat': 0, 
            'val': 255,
            'on' : True
        }
    
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


    # duration might be a global setting
    # thus it might not be processed by Light
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


    def dim_light(self):
        if self.override_hue:
            hue = self.dimmed_hue
        else:
            hue = None
      
        self.set_light(hue, None, self.dimmed_brightness, self.dim_time)


    def brighter_light(self):
        if self.override_undim_brightness:
            brightness = self.undim_brightness
        else:
            brightness = self.start_setting['bri']

        if not self.livingwhite:
            saturation = self.start_setting['sat']

        if self.override_hue:
            hue = self.undim_hue
        else:
            hue = self.start_setting['hue']
        else:
            saturation = None
            hue        = None

    self.set_light(hue, sat, bri, self.dim_time)

    
    def flash_light(self):
        self.dim_light()
        time.sleep(self.dim_time / 10)
        self.brighter_light()


  def partial_light(self):
    if self.override_paused:
      brightness = self.paused_brightness
      if not self.livingwhite:
        saturation = self.start_setting['sat']

        if self.override_hue:
          hue = self.undim_hue
        else:
          hue = self.start_setting['hue']
      else:
        saturation = None
        hue = None
      
      self.set_light(hue, saturation, brightness, self.dim_time)
    else:
      #not enabled for dimming on pause
      self.brighter_light()
