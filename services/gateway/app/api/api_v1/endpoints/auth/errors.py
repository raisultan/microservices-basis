from typing import Final


class AuthError:
    INCORRECT_CREDS: Final[str] = 'Incorrect email or password'
    INACTIVE_USER: Final[str] = 'Inactive user'
