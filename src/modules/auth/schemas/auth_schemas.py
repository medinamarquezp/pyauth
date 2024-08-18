signup_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "last_name": {"type": "string"},
        "email": {"type": "string", "pattern": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"},
        "password": {"type": "string", "minLength": 8,  "pattern": "^(?=.*[A-Za-z])(?=.*\\d)(?=.*[#@$!%*?&^()_+\\-=\\[\\]{}|;:,./~!])[A-Za-z\\d#@$!%*?&^()_+\\-=\\[\\]{}|;:,./~!]{8,}$"},
    },
    "required": ["email", "password"],
}

signin_schema = {
    "type": "object",
    "properties": {
        "email": {"type": "string", "format": "email"},
        "password": {"type": "string"},
    },
    "required": ["email", "password"],
}
