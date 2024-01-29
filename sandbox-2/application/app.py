from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def index():
    return jsonify(output="You found me!")


if __name__ == '__main__':
    app.run(debug=True, port=5002, host='0.0.0.0')
