from datetime import datetime, timedelta, timezone
from typing import Optional
import jwt
import bcrypt
import os

SECRET_KEY = os.getenv("SECRET_KEY", "super_secret_key_for_sallijang_app")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """평문 비밀번호와 bcrypt 해시값을 비교하여 일치 여부를 반환합니다."""
    return bcrypt.checkpw(
        plain_password.encode('utf-8'),
        hashed_password.encode('utf-8')
    )


def get_password_hash(password: str) -> str:
    """비밀번호를 bcrypt로 해싱하여 반환합니다."""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """JWT 액세스 토큰을 생성합니다. expires_delta 미지정 시 15분 유효."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
