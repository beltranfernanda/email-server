import logging

from flask_cors import CORS
from flask import Flask
from app.router.router import map_routes


def create_app():
    flask_app = Flask(__name__)
    logger = flask_app.logger
    logger.setLevel(logging.ERROR)
    map_routes(flask_app)
    return flask_app


if __name__ == "__main__":
    app = create_app()
    CORS(app)
    app.run(debug=False, port=8080)
