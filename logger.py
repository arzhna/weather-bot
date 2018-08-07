from flask import request
import logging
import logging.handlers


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


def init(app, conf):
    # set log level
    app.logger.setLevel(logging.DEBUG if conf.debug else logging.INFO)

    # set format
    log_format = '%(asctime)s | (%(level)s) | %(remote_addr)s | ' \
                 '%(method)s | %(url)s | %(message)s'''
    date_format = '%b %-d %H:%M:%S'
    formatter = LogFormatter(log_format, datefmt=date_format)

    # calculate max size of a log file
    file_handler = logging.handlers.RotatingFileHandler(
        filename=conf.logfile, maxBytes=10000, backupCount=1)

    file_handler.setFormatter(formatter)
    app.logger.addHandler(file_handler)
