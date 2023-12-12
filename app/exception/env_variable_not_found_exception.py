class EnvVariableNotFoundException(Exception):
    def __init__(self, message="Environment variable value not found"):
        self.message = message
        super().__init__(self.message)
