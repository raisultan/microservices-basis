from typing import Final


class DBError:
    INVALID_CREDS: Final[str] = 'Could not validate credentials'
    USER_NOT_FOUND: Final[str] = 'User was not found'
    INACTIVE_USER: Final[str] = 'User is inactive'
    NOT_SUPERUSER: Final[str] = 'The user does not have enough privileges'
