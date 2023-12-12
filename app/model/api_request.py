from typing import TypedDict


class ApiRequest(TypedDict):
    name: str
    email: str
    phone: str
    message: str
