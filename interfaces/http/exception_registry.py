from fastapi.responses import JSONResponse
from fastapi import Request, HTTPException

# Importa las excepciones de cada contexto
from contexts.auth.domain.exceptions.invalid_password_exception import InvalidPasswordException as AuthInvalidPassword
from contexts.users.domain.exceptions.invalid_password_exception import InvalidPasswordException as UsersInvalidPassword

# Mapeo de excepciones a respuestas HTTP
ERROR_MAP = {
    AuthInvalidPassword: (400, "Email o contraseña inválidos."),
    UsersInvalidPassword: (400, "La contraseña no cumple con los requisitos.")
}

# Manejador genérico de excepciones conocidas
async def handle_known_exceptions(_: Request, exc: Exception):
    for exc_type, (status_code, message) in ERROR_MAP.items():
        if isinstance(exc, exc_type):
            return JSONResponse(
                status_code=status_code,
                content={"message": message}
            )

    if isinstance(exc, HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"message": exc.detail}
        )

    # Excepción desconocida
    return JSONResponse(
        status_code=500,
        content={"error": "Ha ocurrido un error inesperado."}
    )
