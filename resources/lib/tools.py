import time
import os
import socket
import json
import random
import hashlib
NOSE = os.environ.get('NOSE', None)
if not NOSE:
  import xbmc
  import xbmcaddon

  __addon__      = xbmcaddon.Addon()
  __cwd__        = __addon__.getAddonInfo('path')
  __icon__       = os.path.join(__cwd__,'icon.png')
  __settings__   = os.path.join(__cwd__,'resources','settings.xml')
  __xml__        = os.path.join( __cwd__, 'addon.xml' )


def notify(title, msg=''):
  if not NOSE:
    global __icon__
    xbmc.executebuiltin( 
      'XBMC.Notification({!s}, {!s}, 3, {!s})'.format(title, msg, __icon__) 
    )

try:
  import requests
except ImportError:
  notify('Kodi Hue', 'ERROR: Could not import Python requests')


def get_version():
  # prob not the best way...
  global __xml__
  try:
    for line in open(__xml__):
      if line.find('ambilight') != -1 and line.find('version') != -1:
        return line[line.find('version=')+9:line.find(' provider')-1]
  except:
    return 'unknown'


def register_user(hue_ip):
  username = hashlib.md5(str(random.random())).hexdigest()
  device = 'xbmc-player'
  data = '{"username": "{!s}", "devicetype": "{!s}"}'.format(username, device)

  r = requests.post('http://{!s}/api'.format(hue_ip), data=data)
  response = r.text
  while 'link button not pressed' in response:
    notify('Bridge discovery', 'press link button on bridge')
    r = requests.post('http://{!s}/api'.format(hue_ip), data=data)
    response = r.text
    time.sleep(3)

  return username




