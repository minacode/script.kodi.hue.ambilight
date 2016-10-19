from Logger import Logger

class Hue:
  
    bridge = None
    lights = {}
    groups = {}
    logger = Logger()
  
    params     = None
    connected  = None
    last_state = None
    light      = None
    dim_group  = None


    def __init__(self, settings, args):
        self.settings = settings
        self._parse_argv(args)
    
        if self.settings.bridge_user not in ['-', '', None]:
            self.update_settings()
    
        if self.params == {}:
            if self.settings.bridge_ip not in ['-', '', None]:
                self.test_connection()
        elif self.params['action'] == 'discover':
            self.logger.debuglog('Starting discover')
            notify('Bridge discovery', 'starting')
            hue_ip = self.start_autodiscover()
            if hue_ip != None:
                notify('Bridge discovery', 'Found bridge at: %s' % hue_ip)
                username = register_user(hue_ip)
                self.logger.debuglog('Updating settings')
                self.settings.update(bridge_ip = hue_ip)
                self.settings.update(bridge_user = username)
                notify('Bridge discovery', 'Finished')
                self.test_connection()
                self.update_settings()
            else:
                notify('Bridge discovery', 'Failed. Could not find bridge.')
        else:
            # not yet implemented
            self.logger.debuglog('unimplemented action call: {!s}'.format(self.params['action']))
    
        if self.connected:
            if self.settings.misc_initialflash:
                self.flash_lights()
  
  
    def start_autodiscover(self):
        port = 1900
        ip = '239.255.255.250'
  
        address = (ip, port)
        data = '''M-SEARCH * HTTP/1.1
                  HOST: {!s}:{!s}
                  MAN: ssdp:discover
                  MX: 3
                  ST: upnp:rootdevice'''.format(ip, port)
                  
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
        hue_ip = None
        num_retransmits = 0
        while(num_retransmits < 10) and hue_ip == None:
            num_retransmits += 1
            client_socket.sendto(data, address)
            recv_data, addr = client_socket.recvfrom(2048)
            self.logger.debuglog('received data during autodiscovery: '+recv_data)
            if 'IpBridge' in recv_data and 'description.xml' in recv_data:
              hue_ip = recv_data.split('LOCATION: http://')[1].split(':')[0]
            time.sleep(1)
    
        if hue_ip is None:
            # still nothing found, try alternate api
            # verify false hack until meethue fixes their ssl cert.
            r = requests.get('https://www.meethue.com/api/nupnp', verify = False)
            j = r.json()
            if len(j) > 0:
                hue_ip = j[0]['internalipaddress']
                self.logger.debuglog('meethue api returned: ' + hue_ip)
            else:
                self.logger.debuglog('meethue api did not find bridge')
            
        return hue_ip
  
  
    def flash_lights(self) -> None:
        self.logger.debuglog('class Hue: flashing lights')
        if self.settings.light == 0:
            self.light.flash_light()
        else:
            self.light[0].flash_light()
            if self.settings.light > 1:
                xbmc.sleep(1)
                self.light[1].flash_light()
            if self.settings.light > 2:
                xbmc.sleep(1)
                self.light[2].flash_light()
  
      
    def _parse_argv(self, args : str) -> None:
        try:
            self.params = { arg.split('=') for arg in args.split('&') }
        except:
            self.params = {}
  
  
    def test_connection(self):
        r = requests.get('http://{!s}/api/{!s}/config'.format(
              self.settings.bridge_ip, self.settings.bridge_user))
        test_connection = r.text.find('name')
        if test_connection:
            notify('Kodi Hue', 'Connected')
            self.connected = True
        else:
            notify('Failed', 'Could not connect to bridge')
            self.connected = False

  
    def lights_do(self, f : Callable[[], None]) -> None:
        if self.settings.light == 0:
            getattr(self.light, f)()
        else:
            m = min(self.settings.light, len(self.light))
            for i in range(0, m):
                getattr(self.light[i], f)()
                xbmc.sleep(1)

  
    def dim_lights(self) -> None:
        self.logger.debuglog('class Hue: dim lights')
        self.last_state = 'dimmed'
        self.lights_do('dim_light')

          
    def brighter_lights(self) -> None:
        self.logger.debuglog('class Hue: brighter lights')
        self.last_state = 'brighter'
        self.lights_do('brighter_light')

  
    def partial_lights(self) -> None:
        self.logger.debuglog('class Hue: partial lights')
        self.last_state = 'partial'
        self.lights_do('partial_light')

      
    def update_settings(self):
        self.logger.debuglog('class Hue: update settings')
        self.logger.debuglog(settings)
        
        if self.settings.light == 0 and \
              (self.light is None or type(self.light) != Group):
            self.logger.debuglog('creating Group instance')
            self.light = Group(self.settings)
        elif self.settings.light > 0 and \
              (self.light is None or \
               type(self.light) == Group or \
               len(self.light) != self.settings.light or \
              self.light[0].light != self.settings.light1_id or \
              (self.settings.light > 1 and self.light[1].light != self.settings.light2_id) or \
              (self.settings.light > 2 and self.light[2].light != self.settings.light3_id)):
            self.logger.debuglog('creating Light instances')
            self.light = [None] * self.settings.light
            self.light[0] = Light(self.settings.light1_id, self.settings)
            if self.settings.light > 1:
                xbmc.sleep(1)
                self.light[1] = Light(self.settings.light2_id, self.settings)
            if self.settings.light > 2:
                xbmc.sleep(1)
                self.light[2] = Light(self.settings.light3_id, self.settings)
  
