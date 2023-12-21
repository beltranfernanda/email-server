import http
from http import HTTPStatus
from typing import Union

from flask import request, jsonify, Response, current_app
from app.exception.email_internal_error_exception import EmailInternalErrorException
from app.model.api_request import ApiRequest
from app.model.api_response import ApiResponse
from app.service.mail import EmailService


class EmailController:
    def __init__(self, email_service: EmailService):
        self.email_service = email_service

    def send_mail(self) -> Union[tuple[Response, HTTPStatus], Response]:
        body: ApiRequest = request.get_json()
        is_valid_body, field = self._validate_api_request(body)

        if not is_valid_body:
            response = ApiResponse(
                400, f"Field {field} is required"
            ).get_formatted_response()
            return jsonify(response), http.HTTPStatus.BAD_REQUEST

        try:
            self.email_service.send_message(
                body["name"], body["email"], body.get("phone", ""), body["message"]
            )
            response = ApiResponse(
                200, "Everything works fine!"
            ).get_formatted_response()
            return jsonify(response), http.HTTPStatus.OK

        except (EmailInternalErrorException, Exception) as err:
            logger = current_app.logger
            logger.error(f"An error occurred in send_email handler: {str(err)}")
            logger.exception("Here information about stacktrace:")
            response = ApiResponse(
                500, f"Internal server error: {err}"
            ).get_formatted_response()
            return jsonify(response), http.HTTPStatus.INTERNAL_SERVER_ERROR

    def _validate_api_request(self, body) -> (bool, str):
        required_fields = ["name", "email", "message"]
        for field in required_fields:
            if field not in body:
                return False, field

        return True, None
