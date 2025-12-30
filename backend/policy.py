import re

def validate_password(pw: str) -> tuple:
    if len(pw) < 12:
        return False, "Password must be at least 12 characters"

    if not re.search(r"[A-Z]", pw):
        return False, "Add an uppercase letter"

    if not re.search(r"[a-z]", pw):
        return False, "Add a lowercase letter"

    if not re.search(r"[0-9]", pw):
        return False, "Add a number"

    if not re.search(r"[!@#$%^&*]", pw):
        return False, "Add a special character"

    return True, "Strong password"
