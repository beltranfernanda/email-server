import base64
import hashlib
import hmac

from flask import request, jsonify

from app.config.config import Config


class AuthMiddleware:
    def __init__(self, view_func, config: Config):
        self.view_func = view_func
        self.__name__ = view_func.__name__
        self.config = config

    def __call__(self, *args, **kwargs):
        if "Authorization" not in request.headers:
            return jsonify({"error": "Unauthorized"}), 401

        if not self.verify_hmac(request.headers, request.path):
            return jsonify({"error": "Invalid HMAC signature"}), 403

        return self.view_func(*args, **kwargs)

    def verify_hmac(self, headers, path):
        received_hmac = request.headers.get("Authorization")
        message = f"{path}&{headers.get('origin', '')}"
        message_bytes = message.encode("utf-8")
        key = self.config.get_param("SECRET_KEY").encode("utf-8")
        hmac_instance = hmac.new(key, message_bytes, hashlib.sha256)
        expected_hmac = base64.b64encode(hmac_instance.digest()).decode()
        return hmac.compare_digest(expected_hmac, received_hmac)
