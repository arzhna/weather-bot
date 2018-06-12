# -*- coding: utf-8 -*-
from enum import Enum
import requests


class DustClass:
    def __init__(self, index, name, min10, max10, min25, max25, emoji):
        self.index = index
        self.name = name
        self.min10 = min10
        self.max10 = max10
        self.min25 = min25
        self.max25 = max25
        self.emoji = emoji


class DustGrade(Enum):
    BEST = DustClass(0, '최고', 0, 15, 0, 8, ':heart_eyes:')
    PRETTY_GOOD = DustClass(1, '좋음', 16, 30, 9, 15, ':blush:')
    GOOD = DustClass(2, '양호', 31, 40, 16, 20, ':slightly_smiling_face:')
    NORMAL = DustClass(3, '보통', 41, 50, 21, 25, ':neutral_face:')
    BAD = DustClass(4, '나쁨', 51, 75, 26, 37, ':weary:')
    FAIRLY_BAD = DustClass(5, '상당히 나쁨', 76, 100, 38, 50, ':angry:')
    VERY_BAD = DustClass(6, '매우 나쁨', 101, 150, 51, 75, ':imp:')
    AWFUL = DustClass(7, '최악', 151, 1000, 76, 1000, ':skull_and_crossbones:')
    UNKNOWN = DustClass(8, '알수없음', -1, -1, -1, -1, ':zipper_mouth_face:')


def _get_dust_grade(value, type=10):
    for grade in DustGrade:
        if type == 10:
            if value >= grade.value.min10 and value <= grade.value.max10:
                return grade.value
        else:
            if value >= grade.value.min25 and value <= grade.value.max25:
                return grade.value

    return DustGrade.UNKNOWN.value


def _get_default_best_value(type=10):
    best = DustGrade.BEST.value
    return (best.max10 + best.min10) / 2 \
        if type == 10 else (best.max25 + best.min25) / 2


def _get_dust_value(raw_data, type=10):
    type_str = 'pm10Value' if type == 10 else 'pm25Value'

    if raw_data['list'][0][type_str] == '-':
        return _get_default_best_value(type)
    else:
        return int(raw_data['list'][0][type_str])


def _get_dust_type_name(type=10):
    return '미세먼지(PM10)' if type == 10 else '초미세먼지(PM25)'


def _get_fmt_data(raw_data):
    dust_types = [10, 25]
    dust_data = ''
    for type in dust_types:
        value = _get_dust_value(raw_data, type)
        grade = _get_dust_grade(value, type)
        dust_data += '{}\t: {} {} {}µg/m³\n'.format(
            _get_dust_type_name(type), grade.emoji, grade.name, value)
    return dust_data


def _get_url(conf):
    return '{}?stationName={}&dataTerm={}&pageNo={}&numOfRows={}' \
           '&ServiceKey={}&ver={}&_returnType={}'.format(
            conf.dust_url, conf.station, conf.data_term, conf.page_no,
            conf.num_of_rows, conf.service_key, conf.version,
            conf.return_type
            )


def get_data(conf):
    dust_url = _get_url(conf)
    res = requests.get(dust_url)
    return _get_fmt_data(res.json()) if res.status_code == 200 else None
