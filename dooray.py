import json
import requests


def send_data(conf, wttr_data):
    req_header = {'Content-Type': 'application/json'}
    res = requests.post(conf.hook_url, json=wttr_data, headers=req_header)
    if res.status_code != 200:
        print json.dumps(res.json(), indent=4, separators=(',', ': '))


def get_fmt_data(conf, data, code_block=True):
    fmt_data = '```%s```' % data if code_block else data
    return {
        'botName': conf.bot_name,
        'botIconImage': conf.icon_url,
        'text': fmt_data
    }
