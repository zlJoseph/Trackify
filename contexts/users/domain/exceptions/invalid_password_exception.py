class InvalidPasswordException(ValueError):
    def __init__(self, message: str = "La contraseña no es válida"):
        super().__init__(message)