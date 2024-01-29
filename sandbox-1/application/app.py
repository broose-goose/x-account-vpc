from random import randrange
from flask import Flask, render_template, jsonify
from os import getenv
from logging import getLogger, INFO
import requests


logger = getLogger(__name__)
logger.setLevel(INFO)

app = Flask(__name__)
sandbox_2_url = getenv('SANDBOX_2', None)


@app.route("/sandbox-2")
def sandbox_2():
    if sandbox_2_url is None:

        return jsonify("SANDBOX_2 NOT SET"), 501

    try:
        headers = {'Content-type': 'text/html; charset=UTF-8'}
        response = requests.get(sandbox_2_url, headers=headers)
        if not response.ok:
            return jsonify("FAILED TO FETCH FROM SANDBOX_2"), 500
        return response.json()
    except Exception as ex:
        logger.error(ex);
        return jsonify("FAILED TO FETCH FROM SANDBOX_2"), 500


@app.route("/sandbox-1")
def sandbox_1():
    return jsonify(output=randrange(1, 10))


@app.route("/")
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, port=5001, host='0.0.0.0')
