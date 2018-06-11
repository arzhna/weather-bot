# -*- coding: utf-8 -*-
from config import Config
import dooray
import dust
import sys
import wttr


# Entry Point
if __name__ == '__main__':
    conf = Config.load(Config.get_config_path(sys.argv))

    wttr_data = wttr.get_data(conf)
    if wttr_data:
        fmt_data = dooray.get_fmt_data(conf, wttr_data)
        dooray.send_data(conf, fmt_data)

    dust_data = dust.get_data(conf)
    if dust_data:
        fmt_data = dooray.get_fmt_data(conf, dust_data)
        dooray.send_data(conf, fmt_data)
