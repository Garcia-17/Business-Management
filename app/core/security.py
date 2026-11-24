import hashlib
import hmac
import secrets

import jwt
from pydantic.types import SecretStr


def generate_salt(size: int = 16) -> bytes:
    return secrets.token_bytes(size)


def hash_password(password: SecretStr, salt: bytes) -> bytes:
    return hashlib.pbkdf2_hmac(
        "sha256", password.get_secret_value().encode(), salt, 600_000
    )


def verify_password(user_password_hash: bytes, provided_password_hash: bytes) -> bool:
    return hmac.compare_digest(user_password_hash, provided_password_hash)


def generate_token(payload: dict, secret: SecretStr):
    return jwt.encode(payload, secret.get_secret_value(), algorithm="HS256")


def decode_token(token: str, secret: SecretStr):
    return jwt.decode(token, secret.get_secret_value(), algorithms=["HS256"])
