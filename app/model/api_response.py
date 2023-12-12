class ApiResponse:
    code: int
    message: str

    def __init__(self,
                 code: int,
                 message: str) -> None:
        super().__init__()
        self.code = code
        self.message = message

    def get_formatted_response(self):
        return {"code": self.code, "message": self.message}
