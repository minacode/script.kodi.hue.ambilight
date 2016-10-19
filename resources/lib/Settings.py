import sys
import xbmcaddon

__addon__      = sys.modules[ '__main__' ].__addon__

class Settings():
  def __init__( self, *args, **kwargs ):
    self.readxml()
    self.addon = xbmcaddon.Addon()

  def readxml(self):
    self.bridge = {
      'ip'   : __addon__.getSetting('bridge_ip'),
      'user' : __addon__.getSetting('bridge_user')
    }
    self.mode                  = int(__addon__.getSetting('mode'))
    self.light                 = int(__addon__.getSetting('light'))
    self.group_id              = int(__addon__.getSetting('group_id'))
    self.misc_initialflash     = __addon__.getSetting('misc_initialflash') == 'true'
    self.misc_disableshort     = __addon__.getSetting('misc_disableshort') == 'true'

    self.dimmed_bri            = int(int(__addon__.getSetting('dimmed_bri').split('.')[0])*254/100)
    self.override_undim_bri    = __addon__.getSetting('override_undim_bri') == 'true'
    self.undim_bri             = int(int(__addon__.getSetting('undim_bri').split('.')[0])*254/100)
    self.override_paused       = __addon__.getSetting('override_paused') == 'true'
    self.paused_bri            = int(int(__addon__.getSetting('paused_bri').split('.')[0])*254/100)
    self.dim_time              = int(float(__addon__.getSetting('dim_time'))*10)
    self.override_hue          = __addon__.getSetting('override_hue') == 'true'
    self.dimmed_hue            = int(__addon__.getSetting('dimmed_hue').split('.')[0])
    self.undim_hue             = int(__addon__.getSetting('undim_hue').split('.')[0])
    self.color_bias            = int(int(__addon__.getSetting('color_bias').split('.')[0])/3*3)

    self.light_id = { 
      1 : int(__addon__.getSetting('light1_id')),
      2 : int(__addon__.getSetting('light2_id')),
      3 : int(__addon__.getSetting('light3_id'))
    }
    self.ambilight = { 
      'dim'       : __addon__.getSetting('ambilight_dim') == 'true',
      'dim_group' : int(__addon__.getSetting('ambilight_dim_group')),
      'min'       : int(int(__addon__.getSetting('ambilight_min').split('.')[0])*254/100),
      'max'       : int(int(__addon__.getSetting('ambilight_max').split('.')[0])*254/100)
    }



    if self.ambilight_min > self.ambilight_max:
        self.ambilight_min = self.ambilight_max
        __addon__.setSetting('ambilight_min', __addon__.getSetting('ambilight_max'))

    self.debug                 = __addon__.getSetting('debug') == 'true'

  def update(self, **kwargs):
    self.__dict__.update(**kwargs)
    for k, v in kwargs.iteritems():
      self.addon.setSetting(k, v)

  def __repr__(self):
    return '''bridge_ip: {bridge_ip!s}
      bridge_user: {bridge_user!s}
      mode: {mode!s} 
      light: {light!s}
      light1_id: {light1_id!s}
      light2_id: {light2_id!s}
      light3_id: {light3_id!s}
      group_id: {group_id!s}
      misc_initialflash: {misc_initialflash!s}
      misc_disableshort: {misc_disableshort!s}
      dimmed_bri: {dimmed_bri!s}
      undim_bri: {undim_bri!s}
      override_paused: {override_paused!s}
      paused_bri: {paused_bri!s}
      dimmed_hue: {dimmed_hue!s}
      override_hue: {override_hue!s}
      undim_hue: {undim_hue!s}
      ambilight_dim: {ambilight_dim!s}
      ambilight_dim_group: {ambilight_dim_group!s}
      ambilight_min: {ambilight_min!s}
      ambilight_max: {ambilight_max!s}
      color_bias: {color_bias!s}
      debug: {debug!s}'''.format( 
        bridge_ip                = self.bridge_ip,
        bridge_user              = self.bridge_user,
        mode                     = self.mode,
        light                    = self.light,
        light1_id                = self.light1_id,
        light2_id                = self.light2_id,
        light3_id                = self.light3_id,
        group_id                 = self.groud_id,
        misc_intial_flash        = self.misc_initial_flash,
        misc_disableshort        = self.misc_disableshort,
        dimmed_bri               = self.disable_bri,
        undim_bri                = self.undim_bri,
        override_paused          = self.override_paused,
        paused_bri               = self.paused_bri,
        dimmed_hue               = self.dimmed_hue,
        override_hue             = self.override_hue,
        undim_hue                = self.undim_hue,
        ambilight_dim            = self.amiblight_dim,
        ambilight_dim_group      = self.ambilight_dim_group,
        ambilight_min            = self.ambilight_min,
        ambilight_max            = self.ambilight_max,
        color_bias               = self.color_bias,
        debug                    = self.debug
      )
