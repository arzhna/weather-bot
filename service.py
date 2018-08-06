from config import Config
from flask import Flask
from flask import jsonify
from flask import request

import dust
import logging
import sys
import wttr


app = Flask(__name__)
conf = Config.load(Config.get_config_path(sys.argv))


@app.route("/wttr", methods=['GET', 'POST'])
def get_weather():
    wttr_data = wttr.get_data(conf, current=True)
    return jsonify(text=wttr_data, response_type="inChannel")


@app.route("/dust", methods=['GET', 'POST'])
def get_dust():
    dust_data = dust.get_data(conf)
    return jsonify(text=dust_data, response_type="inChannel")


@app.after_request
def after(response):
    app.logger.info(response.status_code)
    return response


class LogFormatter(logging.Formatter):
    def format(self, record):
        levels = {
            logging.DEBUG: 'DEBG',
            logging.INFO: 'INFO',
            logging.WARNING: 'WARN',
            logging.ERROR: 'ERRO',
            logging.CRITICAL: 'FATL'
        }
        if record.levelno in levels:
            record.level = levels[record.levelno]
        record.remote_addr = request.remote_addr
        record.url = request.url
        record.method = request.method
        return logging.Formatter.format(self, record)


def log_init():
    print conf.logfile
    # set log level
    app.logger.setLevel(logging.DEBUG if conf.debug else logging.INFO)

    # set format
    log_format = '%(asctime)s | (%(levelno)s) | %(remote_addr)s | ' \
                 '%(method)s | %(url)s | %(message)s'''
    date_format = '%b %-d %H:%M:%S'
    formatter = LogFormatter(log_format, datefmt=date_format)

    # calculate max size of a log file
    file_handler = logging.handlers.RotatingFileHandler(
        filename=conf.logfile, maxBytes=10000, backupCount=1)
    file_handler.setFormatter(formatter)
    app.logger.addHandler(file_handler)


# Entry Point
if __name__ == '__main__':
    log_init()
    app.run(host='0.0.0.0', port=6161, debug=True)
