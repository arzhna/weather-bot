import requests


def __remove_last_lines_from_string(str, count):
    return str if count <= 0 else \
        __remove_last_lines_from_string(str[:str.rfind('\n')], count - 1)


def __get_url(conf, current=False):
    opt = "0T" if current else conf.wttr_opt
    # http://wttr.in/seoul?1Tn
    return '{}/{}?{}'.format(conf.wttr_url, conf.location, opt)


def get_data(conf, current=False):
    wttr_url = __get_url(conf, current)
    res = requests.get(wttr_url)
    if res.status_code == 200:
        reduce_lines = 0 if current else 4
        return __remove_last_lines_from_string(res.content, reduce_lines)
    else:
        return None
