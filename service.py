from config import Config
from flask import Flask
from flask import jsonify

import dust
import logger
import sys
import wttr


app = Flask(__name__)
conf = Config.load(Config.get_config_path(sys.argv))
logger.init(app, conf)


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


# Entry Point
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6161, debug=True)
