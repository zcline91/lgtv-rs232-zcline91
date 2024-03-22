import serial


class LgTV():
    _commands = {
        'power': 'ka',
        'input': 'xb',
        'aspect': 'kc',
        'screen_mute': 'kd',
        'sound': 'ke',
        'volume': 'kf',
        'contrast': 'kg',
        'brightness': 'kh',
        'color': 'ki',
        'tint': 'kj',
        'sharpness': 'kk',
        'osd': 'kl',
        'control_lock': 'km',
        'treble': 'kr',
        'bass': 'ks',
        'balance': 'kt',
        '3d': 'xt',
        'color_temp': 'xu',
        'extended_3d': 'xv',
        'energy': 'jq',
        'auto_config': 'ju',
        'channel_tuning': 'ma',
        'channel_add_del': 'mb',
        'key': 'mc',
        'backlight': 'mg',
        }

    _binary_commands = {
        'power',
        'sound',
        'osd',
        'control_lock',
        'channel_add_del'
    }

    _cent_commands = {
        'volume',
        'contrast',
        'brightness',
        'color',
        'tint',
        'sharpness',
        'treble',
        'bass',
        'balance',
        'color_temp',
        'backlight'
    }

    _other_data = {
        'input': {
            'dtv_ant': '00',
            'dvt_cab': '01',
            'analog_ant': '10',
            'analog_cab': '11', 
            'av1': '20',
            'av2': '21',
            'comp1': '40',
            'comp2': '41',
            'rgb': '60',
            'hdmi1': '90',
            'hdmi2': '91',
            'hdmi3': '92',
            'hdmi4': '93',
        },
        'aspect': {
            '4x3': '01',
            '16x9': '02',
            'set_by_program': '06',
            'just_scan': '09',
            'zoom1': '10',
            'zoom2': '11',
            'zoom3': '12',
            'zoom4': '13',
            'zoom5': '14',
            'zoom6': '15',
            'zoom7': '16',
            'zoom8': '17',
            'zoom9': '18',
            'zoom10': '19',
            'zoom11': '1a',
            'zoom12': '1b',
            'zoom13': '1c',
            'zoom14': '1d',
            'zoom15': '1e',
            'zoom16': '1f',
        },
        'screen_mute': {
            'off': '00',
            'on': '01',
            'vid_out_mute': '10',
        },
        '3d': {
            'tb': '00 00 00 00',
            'sbs_rtl': '00 01 00 00',
            'sbs_ltr': '00 01 01 00',
            'check': '00 02 00 00',
            'frame_sequential': '00 03 00 00',
            'off': '01 00 00 00',
            '3d_2d': '02 00 00 00',
            '2d_3d': '03 00 00 0a',
        },
        'extended_3d': dict(),
        'energy': {
            'off': '00',
            'minimum': '01',
            'medium': '02',
            'maximum': '03',
            'auto': '04',
            'screen_off': '05',
        },
        'auto_config': {'run': '01'},
        'channel_tuning': dict(),
        'key': {
            'power': '08',
            'qmenu': '45',
            'home': '43',
            'input': '0b',
            '0': '10',
            '1': '11',
            '2': '12',
            '3': '13',
            '4': '14',
            '5': '15',
            '6': '16',
            '7': '17',
            '8': '18',
            '9': '19',
            '-': '4c',
            'flashbk': '1a',
            'mute/delete': '09',
            'vol+': '02',
            'vol-': '03',
            'ch+': '00',
            'ch-': '01',
            'fav/mark': '1e',
            'up': '40',
            'down': '41',
            'left': '07',
            'right': '06',
            'enter': '44',
            'back': '28',
            'ratio': '79',
            'energy': '95',
            'simplink': '7e',
            'info': 'aa',
            'av_mode': '30',
            'red': '72',
            'green': '71',
            'yellow': '63',
            'blue': '61',
            'stop': 'b1',
            'play': 'b0',
            'pause': 'ba',
            'fastfwd': '8e',
            'rewind': '8f',
            'tv': '0f',
            '3d': 'dc',
            'exit': '5b',
            'power_on': 'c4',
            'power_off': 'c5',
            'av1': '5a',
            'av2': 'd0',
            'comp1': 'bf',
            'comp2': 'd4',
            'rgb': 'd5',
            'hdmi1': 'ce',
            'hdmi2': 'cc',
            'hdmi3': 'e9',
            'hdmi4': 'da',
            '4x3': '76',
            '16x9': '77',
            'ratio_zoom': 'af',
        },
    }

    def __init__(self, path, update=True):
        # path is a string set to the location of the serial device, 
        # e.g. "/dev/ttyUSB0"
        self._volume = None
        self._muted = None
        self._input = None
        self._sources = sorted(self._other_data['input'].keys())
        self._ser = serial.Serial(path, timeout=2.0, write_timeout=2.0)
        if update and self.is_on:
            self.update_status()

    @property
    def volume(self):
        return self._volume

    @property
    def muted(self):
        return self._muted
    
    @property
    def input(self):
        return self._input

    @property
    def sources(self):
        return self._sources

    @property
    def is_on(self):
        status = self.request('power', 'check')
        if status == 'on':
            return True
        else:
            return False

    def request(self, command, value):
        assert command in self._commands.keys()
        # Build request to send to the TV
        if value == 'check':
            data = 'ff'
        elif command in self._binary_commands: 
            assert value in {'on', 'off'}
            if value == 'off':
                data = '00'
            elif value == 'on':
                data = '01'
        elif command in self._cent_commands:
            assert value in [str(i) for i in range(101)]
            data = hex(int(value))[2:] # Convert integer to OxAB
            if len(data) == 1:
                data = '0' + data
        else:
            assert value in self._other_data[command].keys()
            data = self._other_data[command][value]   
        # For an explanation of the format of the request, see 
        # http://gscs-b2c.lge.com/downloadFile?fileId=6CNJQR84slwAZdSBiw2DA
        request = bytes(
            ' '.join((self._commands[command], '01', data)) + '\n',
            'ascii'
        ) 

        self._ser.write(request)

        response = str(self._ser.read_until(b'x'), 'ascii').strip('x')
        if 'NG' in response or response == '':
            return False
        hexnum = response.split('OK')[1]
        if value == 'check':
            if command in self._binary_commands:
                if hexnum == '00':
                    return 'off'
                elif hexnum == '01':
                    return 'on'
            elif command in self._cent_commands:
                return int('0x' + hexnum, 0) # Convert 0xAB to integer
            else:
                return next(
                    key for key, value in self._other_data[command].items()
                    if value == hexnum
                )
        else:
            if hexnum == data:
                return True
            else:
                return False

    def update_status(self):
        self._input = self.request('input', 'check')
        sound = self.request('sound', 'check')
        if sound == 'off':
            self._muted = True
        else:
            self._muted = False
        self._volume = self.request('volume', 'check')
