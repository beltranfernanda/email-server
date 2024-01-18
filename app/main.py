import logging

from flask import Flask
from app.router.router import map_routes


def create_app():
    app = Flask(__name__)
    logger = app.logger
    logger.setLevel(logging.ERROR)
    map_routes(app)
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=False, port=8080)
