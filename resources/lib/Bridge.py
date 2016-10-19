import json
from Settings import Settings
from Logger   import Logger


class Bridge(Logger):
    
    def __init__(self, ip, user):
        Logger.__init__(self)

        self.ip      = ip
        self.user    = user
        self.session = request.Session()

    def request_url_put(self, url, data):
        try:
            self.session.put(url, data = data)
        except:
            # probably a timeout
            self.debuglog('exception in request_url_put')


    def request_url_get(self, url):
        try:
            return self.session.get(url)
        except:
            # probably a timeout
            self.debuglog('exception in request_url_get')


    def get_light_url(self, light_id):
        return 'http://{!s}/api/{!s}/lights/{}/'.format(
                 self.ip, self.user, light_id
               )


    def send_light_update(self, light, transition_time):
        
        if light.on:
            data = {
                'on'  : True,
                'hue' : light.hue,
                'sat' : light.saturation,
                'bri' : light.bri,
                'transition_time' : transition_time
            }
        else:
            data = {'on' : False}

        data_string = json.dumps(data)
        self.request_url_put(self.get_light_url() + 'state/', data_string)


    def receive_light_update(self, light):
        response = self.request_url_get(self.get_light_url())
        return response.json()
        
 
    def get_group_url(self, group_id):
        return 'http://{!s}/api/{!s}/groups/{}/'.format(
                 self.ip, self.user, group_id
               )


    def send_group_update(self, group, transition_time):
        
        if group.on:
            data = {
                'on'  : True,
                'hue' : group.hue,
                'sat' : group.saturation,
                'bri' : group.bri,
                'transition_time' : transition_time
            }
        else:
            data = {'on' : False}

        data_string = json.dumps(data)
        self.request_url_put(self.get_group_url() + 'action/', data_string)


    def receive_group_update(self, group_id):
        response = self.request_url_get(self.get_group_url())
        return response.json()
