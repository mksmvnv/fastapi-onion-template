from bcrypt import gensalt, hashpw, checkpw


def hash_password(password: str) -> str:
    """Hash a plaintext password using bcrypt.

    Args:
        password (str): The plaintext password to hash.

    Returns:
        str: The hashed password as a string.
    """

    salt = gensalt()
    hashed_password = hashpw(password.encode("utf-8"), salt).decode("utf-8")

    return hashed_password


def verify_password(password: str, hashed_password: str) -> bool:
    """Check if given password matches hashed password.

    Args:
        password (str): Input password.
        hashed_password (str): Hashed password.

    Returns:
        bool: True if password matches, False otherwise.
    """

    check = checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))

    return check
