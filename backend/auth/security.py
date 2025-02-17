from bcrypt import gensalt, hashpw, checkpw


def hash_password(plain_password: str) -> str:
    hashed_password = hashpw(plain_password.encode("utf-8"), gensalt()).decode(
        "utf-8"
    )
    return hashed_password


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )
