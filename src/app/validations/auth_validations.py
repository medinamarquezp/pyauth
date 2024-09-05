import re


def validate_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(pattern, email))


def validate_min_length(password):
    return len(password) >= 8


def validate_password(password):
    pattern = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[#@$!%*?&^()_+\-=\\[\\]{}|;:,./~!])[A-Za-z\d#@$!%*?&^()_+\-=\\[\\]{}|;:,./~!]{8,}$'
    return bool(re.match(pattern, password))
