from Logger import Logger
from Light  import Light


class Group():
  
    hue           = 0
    saturation    = 0
    brightness    = 0
    lights        = {}
    logger        = Logger()
    

    def __init__(self, group_id, bridge, settings):
        self.logger = Logger()
      
        self.id     = settings.group_id
        self.bridge = bridge
        
        self.discover_lights()


    def discover_lights(self):
        data = self.bridge.receive_group_update(self)
        
        for light_id in data['lights']:
            light = Light(light_id, self.bridge, settings) # settings free
            light.get_current_setting()
            if light.start_setting['on']:
                self.lights[light_id] = light
  

    def set_lights(self, hue, saturation, brightness, duration = 0):
        if not self.livingwhite:
            if hue is not None:
                self.hue = hue
            if saturation is not None:
                self.saturation = saturation
    
        if brightness > 0:
            self.on         = True
            self.brightness = brightness
        else:
            self.on         = False
            
        self.bridge.send_group_update(self, duration)


    # def dim_light(self):
    #     for light in self.lights:
    #         self.lights[light].dim_light()
    
    # def brighter_light(self):
    #     for light in self.lights:
    #         self.lights[light].brighter_light()
        
    # def partial_light(self):
    #     for light in self.lights:
    #         self.lights[light].partial_light()
