from typing import Final


class UsersAPIError:
    NOT_FOUND: Final[str] = 'The user with this username does not exist in the system'
    ALREADY_EXISTS: Final[str] = 'The user with this username already exists in the system'
    INACTIVE: Final[str] = 'The user is inactive'
