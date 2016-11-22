# constants are still in here

import sys
import xbmcaddon
from Constants import MODE_THEATRE, MODE_AMBILIGHT

class Settings():

    data = {}

    def __init__(self, ADDON, ADDON_PATH, *args, **kwargs):
        self.ADDON = ADDON
        self.ADDON_PATH = ADDON_PATH

    def __getitem__(self, key):
        try:
            return self.dat[key]
        except:
            return None


    def open_template_file(self, file):
        return open('{path}recources/templates/{file}'.format(
            path = self.ADDON_PATH, file = file))


    def open_settings_file(self, mode = 'w'):
        return open('{path}recources/settings.xml'.format(path = self.ADDON_PATH), mode)


    # need to factor out the template strings
    # need to add language support
    def update_lights(self, lights, groups):
        settings_file = self.open_settings_file()
        light_template = self.open_template_file('LightSetting.xml').readline()
        group_template = self.open_template_file('GroupSetting.xml').readline()

        lines = settings_file.readlines()

        i = 0
        for line in lines:
            if '// LIGHTS START' in line:
                start_index = i
            if '// LIGHTS END' in line:
                end_index = i
            i += 1
        lines = lines[:start_index]

        id = 1
        for light in lights:
            lines.append(light_template.format(id = id, label = light.name))
            id += 1

        id = 1
        for group in groups:
            lines.append(group_template.format(id = id, label = group.name))
            id += 1

        lines += lines[end_index - 1:]
        settings_file.write('\n'.join(lines))


    def read_xml(self):
        self.data['bridge'] = {
            'ip':   self.ADDON.getSetting('bridge_ip'),
            'user': self.ADDON.getSetting('bridge_user')
        }
        self.data['mode'] = int(self.ADDON.getSetting('mode'))

        self.data['misc_initialflash'] = self.ADDON.getSetting('misc_initialflash') == 'true'
        self.data['misc_disableshort'] = self.ADDON.getSetting('misc_disableshort') == 'true'

        self.dimmed_bri = (float(self.ADDON.getSetting('dimmed_bri')) * 254) // 100
        self.override_undim_bri = self.ADDON.getSetting('override_undim_bri') == 'true'
        self.undim_bri = (float(self.ADDON.getSetting('undim_bri')) * 254) // 100
        self.override_paused = self.ADDON.getSetting('override_paused') == 'true'
        self.paused_bri = (float(self.ADDON.getSetting('paused_bri')) * 254) // 100
        self.dim_time = int(float(self.ADDON.getSetting('dim_time'))) * 10
        self.override_hue = self.ADDON.getSetting('override_hue') == 'true'
        self.dimmed_hue = int(float(self.ADDON.getSetting('dimmed_hue')))
        self.undim_hue = int(float(self.ADDON.getSetting('undim_hue')))
        self.color_bias = (float(self.ADDON.getSetting('color_bias'))) // 9

        # change
        self.light_id = {
            1: int(self.ADDON.getSetting('light1_id')),
            2: int(self.ADDON.getSetting('light2_id')),
            3: int(self.ADDON.getSetting('light3_id'))
        }

        self.data['ambilight'] = {
            'dim': self.ADDON.getSetting('ambilight_dim') == 'true',
            'dim_group': int(self.ADDON.getSetting('ambilight_dim_group')),
            'min': int(int(self.ADDON.getSetting('ambilight_min').split('.')[0]) * 254 / 100),
            'max': int(int(self.ADDON.getSetting('ambilight_max').split('.')[0]) * 254 / 100)
        }

        if self['ambilight']['min'] > self['ambilight']['max']:
            self['ambilight']['min'] = self['ambilight']['max']
            self.ADDON.setSetting('ambilight_min', self.ADDON.getSetting('ambilight_max'))

        self.data['debug'] = self.ADDON.getSetting('debug') == 'true'


    # scary
    def update(self, **kwargs):
        self.__dict__.update(**kwargs)
        for k, v in kwargs.iteritems():
            self.ADDON.setSetting(k, v)


    def __repr__(self):
        return get_representation(self.data)


    def get_representation(self, data, path = ''):
        rep = ''
        for (key, value) in seld.data.items():
            if type(value) is dict:
                rep += self.get_representation(value, str(key))
            else:
                rep += '{key!s}: {path}_{value!s}'.format(
                        key = key, path = path, value = value)
            rep += '\n'
        return rep
