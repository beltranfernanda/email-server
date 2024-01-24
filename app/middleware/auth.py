import base64
import hashlib
import hmac
import http

from flask import request, jsonify

from app.config.config import Config
from app.model.api_response import ApiResponse


class AuthMiddleware:
    def __init__(self, view_func, config: Config):
        self.view_func = view_func
        self.__name__ = view_func.__name__
        self.config = config

    def __call__(self, *args, **kwargs):
        if "Authorization" not in request.headers:
            response = ApiResponse(
                http.HTTPStatus.UNAUTHORIZED, "Unauthorized user"
            ).get_formatted_response()
            return jsonify(response), http.HTTPStatus.UNAUTHORIZED

        if not self.verify_hmac(request.headers, request.path):
            response = ApiResponse(
                http.HTTPStatus.FORBIDDEN, "Invalid user credentials"
            ).get_formatted_response()
            return jsonify(response), http.HTTPStatus.FORBIDDEN

        return self.view_func(*args, **kwargs)

    def verify_hmac(self, headers, path):
        received_hmac = request.headers.get("Authorization")
        message = f"{path}&{headers.get('x-origin', '')}"
        message_bytes = message.encode("utf-8")
        key = self.config.get_param("SECRET_KEY").encode("utf-8")
        hmac_instance = hmac.new(key, message_bytes, hashlib.sha256)
        expected_hmac = base64.b64encode(hmac_instance.digest()).decode()
        return hmac.compare_digest(expected_hmac, received_hmac)
