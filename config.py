import ConfigParser


class Config:
    def __init__(self, bot_name, hook_url, icon_url,
                 wttr_url, wttr_opt, location,
                 dust_url, station, data_term, service_key, version,
                 logfile, debug=False):
        self.bot_name = bot_name
        self.hook_url = hook_url
        self.icon_url = icon_url
        self.wttr_url = wttr_url
        self.wttr_opt = wttr_opt
        self.location = location

        self.dust_url = dust_url
        self.station = station
        self.data_term = data_term
        self.page_no = 1
        self.num_of_rows = 1
        self.service_key = service_key
        self.version = version
        self.return_type = 'json'

        self.logfile = logfile
        self.debug = debug

    def __repr__(self):
        return '''Configs:
        bot_name = {}
        hook_url = {}
        icon_url = {}
        wttr_url = {}
        wttr_opt = {}
        location = {}
        dust_url = {}
        stations = {}
        data_term = {}
        service_key = {}
        version = {}
        logfile = {}
        debug = {}
        '''.format(self.bot_name, self.hook_url, self.icon_url,
                   self.wttr_url, self.wttr_opt, self.location,
                   self.dust_url, self.station, self.data_term,
                   self.service_key, self.version,
                   self.logfile, self.debug)

    @staticmethod
    def load(path):
        __section_dooray = 'dooray'
        __section_wttr = 'wttr'
        __section_dust = 'dust'
        __section_debug = 'debug'

        parser = ConfigParser.SafeConfigParser()
        parser.optionxform = str
        if not parser.read(path):
            raise ValueError('No config file found!', path)

        try:
            bot_name = parser.get(__section_dooray, 'bot_name')
            hook_url = parser.get(__section_dooray, 'hook_url')
            icon_url = parser.get(__section_dooray, 'icon_url')

            wttr_url = parser.get(__section_wttr, 'wttr_url')
            wttr_opt = parser.get(__section_wttr, 'wttr_opt')
            location = parser.get(__section_wttr, 'location')

            dust_url = parser.get(__section_dust, 'dust_url')
            station = parser.get(__section_dust, 'station')
            data_term = parser.get(__section_dust, 'data_term')
            service_key = parser.get(__section_dust, 'service_key')
            version = parser.get(__section_dust, 'version')

            logfile = parser.get(__section_debug, 'logfile')
            debug = parser.get(__section_debug, 'debug')

            return Config(bot_name, hook_url, icon_url,
                          wttr_url, wttr_opt, location,
                          dust_url, station, data_term, service_key, version,
                          logfile, debug)

        except ConfigParser.NoOptionError as e:
            print("%s" % e.message)
            return None

    @staticmethod
    def get_default_path():
        return './bot.conf'

    @staticmethod
    def get_config_path(argv):
        return argv[1] if len(argv) > 1 else Config.get_default_path()
