class InvalidPasswordException(Exception):
    def __init__(self, message: str = "Credenciales inválidas"):
        super().__init__(message)