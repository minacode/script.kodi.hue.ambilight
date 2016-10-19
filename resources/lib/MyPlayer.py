import xbmc

class MyPlayer(xbmc.Player):
  duration     = 0
  playingvideo = None

  def __init__(self):
    xbmc.Player.__init__(self)
  
  def onPlayBackStarted(self):
    if self.isPlayingVideo():
      self.playingvideo = True
      self.duration = self.getTotalTime()
      state_changed('started', self.duration)

  def onPlayBackPaused(self):
    if self.isPlayingVideo():
      self.playingvideo = False
      state_changed('paused', self.duration)

  def onPlayBackResumed(self):
    if self.isPlayingVideo():
      self.playingvideo = True
      state_changed('resumed', self.duration)

  def onPlayBackStopped(self):
    if self.playingvideo:
      self.playingvideo = False
      state_changed('stopped', self.duration)

  def onPlayBackEnded(self):
    if self.playingvideo:
      self.playingvideo = False
      state_changed('stopped', self.duration)
