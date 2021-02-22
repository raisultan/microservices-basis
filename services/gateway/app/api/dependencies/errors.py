from typing import Final


class DBError:
    USER_NOT_FOUND: Final[str] = 'User was not found'
    INACTIVE_USER: Final[str] = 'User is inactive'
