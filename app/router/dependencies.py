from flask import Flask

from app.config.config import Config
from app.controller.mail import EmailController
from app.controller.ping import PingController
from app.service.mail import EmailService


def load_dependencies(app: Flask) -> dict:
    ping_controller = PingController()

    config = Config(app)
    config.load_app_config()
    email_service = EmailService(config)
    email_controller = EmailController(email_service)

    return {"ping": ping_controller, "email": email_controller, "config": config}
