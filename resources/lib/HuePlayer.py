import xbmc

class HuePlayer(xbmc.Player):
  DURATION      = 0
  playing_video = None

  def __init__(self):
    xbmc.Player.__init__(self)

  def onPlayBackStarted(self):
    if self.isPlayingVideo():
      self.playing_video = True
      self.DURATION = self.getTotalTime()
      state_changed('started', self.DURATION)

  def onPlayBackPaused(self):
    if self.isPlayingVideo():
      self.playing_video = False
      state_changed('paused', self.DURATION)

  def onPlayBackResumed(self):
    if self.isPlayingVideo():
      self.playing_video = True
      state_changed('resumed', self.DURATION)

  def onPlayBackStopped(self):
    if self.playing_video:
      self.playing_video = False
      state_changed('stopped', self.DURATION)

  def onPlayBackEnded(self):
    if self.playing_video:
      self.playing_video = False
      state_changed('stopped', self.DURATION)
