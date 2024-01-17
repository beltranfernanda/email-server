from flask import Flask

from app.middleware.auth import AuthMiddleware
from app.router.dependencies import load_dependencies


def map_routes(app: Flask) -> None:
    instances = load_dependencies(app)

    ping = AuthMiddleware(instances.get("ping").ping, instances.get("config"))
    app.add_url_rule("/ping", view_func=ping)

    email = AuthMiddleware(instances.get("email").send_mail, instances.get("config"))
    app.add_url_rule("/mail/send", view_func=email, methods=["POST"])
