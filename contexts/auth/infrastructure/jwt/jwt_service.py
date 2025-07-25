import jwt
from datetime import datetime, timedelta, timezone
from shared.config.settings import settings

class JWTService:
    def generate_token(self, data: dict, expires_minutes: int = 60):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, settings.jwt_secret, algorithm="HS256")
