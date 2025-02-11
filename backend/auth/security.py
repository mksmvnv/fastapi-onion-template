from bcrypt import gensalt, hashpw, checkpw

from utils.constants import UTF8


def hash_password(password: str) -> str:
    """Hash a plaintext password using bcrypt.

    Args:
        password (str): The plaintext password to hash.

    Returns:
        str: The hashed password as a string.
    """

    salt = gensalt()
    hashed_password = hashpw(password.encode(UTF8), salt).decode(UTF8)

    return hashed_password


def verify_password(password: str, hashed_password: str) -> bool:
    """Check if given password matches hashed password.

    Args:
        password (str): Input password.
        hashed_password (str): Hashed password.

    Returns:
        bool: True if password matches, False otherwise.
    """

    check = checkpw(password.encode(UTF8), hashed_password.encode(UTF8))

    return check
