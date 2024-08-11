signup_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "last_name": {"type": "string"},
        "email": {"type": "string"},
        "password": {"type": "string"},
    },
    "required": ["email", "password"],
}
