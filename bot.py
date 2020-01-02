#!/usr/bin/python
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
    dust_data = dust.get_data(conf)

    data = ''
    data += wttr_data + '\n' if wttr_data else ''
    data += dust_data if dust_data else ''

    if len(data):
        fmt_data = dooray.get_fmt_data(conf, data)
        dooray.send_data(conf, fmt_data)
