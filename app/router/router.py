from flask import Flask

from app.router.dependencies import load_dependencies


def map_routes(app: Flask) -> None:
    instances = load_dependencies(app)

    ping = instances.get('ping')
    app.add_url_rule("/ping", view_func=ping.ping)

    email = instances.get('email')
    app.add_url_rule("/mail/send", view_func=email.send_mail, methods=['POST'])

