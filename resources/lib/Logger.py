import xbmc
from Settings import SETTINGS

class Logger:
  script_name   = 'Kodi Hue'
  logging       = True
  debug_logging = False


  def __init__(self, debug = False):
      self.debug_logging = debug


  def log(self, message):
    if self.logging:
      xbmc.log('{}: {}'.format(self.script_name, message))


  def debuglog(self, message):
    if self.debug_logging:
      self.log('DEBUG {}'.format(message))


  def endable_debug(self):
    self.debug_logging = True


  def disable_debug(self):
    self.debug_logging = False


  def enable_logging(self):
    self.logging = True


  def disable(self):
    self.logging = False
