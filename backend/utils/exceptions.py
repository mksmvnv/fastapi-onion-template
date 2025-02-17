from fastapi import HTTPException, status


class UserNotFoundError(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_404_NOT_FOUND,
        detail: str = "User not found",
    ):
        super().__init__(status_code=status_code, detail=detail)


class CredentialsAlreadyInUseError(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        detail: str = "Credentials already in use",
    ):
        super().__init__(status_code=status_code, detail=detail)


class PasswordsDoNotMatchError(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        detail: str = "Passwords do not match",
    ):
        super().__init__(status_code=status_code, detail=detail)


class AtLeastOneFieldIsRequiredError(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        detail: str = "At least one field is required",
    ):
        super().__init__(status_code=status_code, detail=detail)
