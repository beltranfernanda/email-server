class EmailInternalErrorException(Exception):
    def __init__(self, message="An error has occurred sending message"):
        self.message = message
        super().__init__(self.message)
