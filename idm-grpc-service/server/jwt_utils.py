import jwt
import uuid
from datetime import datetime, timedelta

SECRET_KEY = "super-secret-key"
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 60


def generate_token(user_id: int, email: str, role: str) -> str:
    payload = {
        "iss": "idm-grpc-service",
        "sub": str(user_id),
        "email": email,
        "role": role,
        "jti": str(uuid.uuid4()),
        "exp": datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_MINUTES),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
