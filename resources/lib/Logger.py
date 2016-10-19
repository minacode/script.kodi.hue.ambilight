import xbmc


class Logger:
  script_name   = 'Kodi Hue'
  logging       = True
  debug_logging = False


  def __init__(self, debug = False) -> None:
      self.debug_logging = debug


  def log(self, message: str) -> None:
    if self.logging:
      xbmc.log('{}: {}'.format(self.script_name, message))


  def debuglog(self, message: str) -> None:
    if self.debug_logging:
      self.log('DEBUG {}'.format(message))


  def endable_debug(self) -> None:
    self.debug_logging = True


  def disable_debug(self) -> None:
    self.debug_logging = False


  def enable_logging(self):
    self.logging = True


  def disable(self) -> None:
    self.logging = False
