from Logger import Logger
from Bridge import Bridge

class Hue:

    bridge = None
    lights = {}
    groups = {}
    logger = Logger()

    def __init__(self, settings, discover):
        if discover:
            self.discover_bridge()

        if self.bridge is not None:
            self.test_connection()
            if self.misc_initialflash:
                self.flash_lights()

    def discover_bridge(self):
        self.logger.debuglog('Starting discover')
        # likely to break, cause of namespace
        notify('Bridge discovery', 'starting')
        ip = self.autodiscover()
        if ip is not None:
            notify('Bridge discovery', 'Found bridge at: {!s}'.format(ip))
            user = self.register_user(ip)
            self.bridge = Bridge(ip = ip, user = user)
            notify('Bridge discovery', 'Finished')
            self.test_connection()
        else:
            notify('Bridge discovery', 'Failed. Could not find bridge.')

    # not good, but good enough for now
    def autodiscover(self):
        port = 1900
        ip = '239.255.255.250'

        address = (ip, port)
        data = '''M-SEARCH * HTTP/1.1
                  HOST: {!s}:{!s}
                  MAN: ssdp:discover
                  MX: 3
                  ST: upnp:rootdevice'''.format(ip, port)

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        num_retransmits = 0
        for retransmit_count in range(10):
            client_socket.sendto(data, address)
            recv_data, addr = client_socket.recvfrom(2048)
            self.logger.debuglog(
                'received data during autodiscovery: ' + recv_data)
            if 'IpBridge' in recv_data and 'description.xml' in recv_data:
                return recv_data.split('LOCATION: http://')[1].split(':')[0]
            time.sleep(1)

        # still nothing found, try alternate api
        # verify false hack until meethue fixes their ssl cert.
        r = requests.get('https://www.meethue.com/api/nupnp', verify = False)
        j = r.json()
        try:
            return j[0]['internalipaddress']
        except:
            self.logger.debuglog('meethue api did not find bridge')
        return None

    def test_connection(self):
        if self.bridge.receive_config() is not None:
            notify('Kodi Hue', 'Connected')
        else:
            notify('Failed', 'Could not connect to bridge')

    def get_lights(self):
        return self.lights.values()

    def lights_do(self):
        for light in self.lights.values():
            getattr(light, f)()
        for group in self.groups.values():
            getattr(group, f)()

    def flash_lights(self):
        self.logger.debuglog('class Hue: flashing lights')
        self.lights_do('flash')

    def dim_lights(self):
        self.logger.debuglog('class Hue: dim lights')
        self.last_state = 'dimmed'
        self.lights_do('dim')

    def brighter_lights(self):
        self.logger.debuglog('class Hue: brighter lights')
        self.last_state = 'brighter'
        self.lights_do('brighter')

    def partial_lights(self):
        self.logger.debuglog('class Hue: partial lights')
        self.last_state = 'partial'
        self.lights_do('partial')

    def update_settings(self, settings):
        self.logger.debuglog('class Hue: update settings')
        self.logger.debuglog(settings)

        if self.settings.light == 0 and \
                (self.light is None or type(self.light) != Group):
            self.logger.debuglog('creating Group instance')
            self.light = Group(self.settings)
        elif self.settings.light > 0 and \
            (self.light is None or
             type(self.light) == Group or
             len(self.light) != self.settings.light or
             self.light[0].light != self.settings.light1_id or
             (self.settings.light > 1 and self.light[1].light != self.settings.light2_id) or
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
