import re

PATTERN = r"(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[^A-Za-z0-9])(?=.{8,})"


def password_strong(password):
    return bool(re.match(PATTERN, password))
