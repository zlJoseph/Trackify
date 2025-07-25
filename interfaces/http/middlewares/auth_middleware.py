import jwt
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from shared.config.settings import settings

security = HTTPBearer()  # Extrae el token del header Authorization: Bearer <token>

def get_current_user_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    token = credentials.credentials
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])
        return payload
    except ExpiredSignatureError as exc:
        raise HTTPException(status_code=401, detail="Sesión expirada") from exc
    except InvalidTokenError as exc:
        raise HTTPException(status_code=401, detail="Sesión inválida") from exc
