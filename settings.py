DEBUG = True
PORT = 8080
SECRET_KEY = "secret"
WTF_CSRF_ENABLED = True

PASSWORDS = {
    "admin": "$pbkdf2-sha256$29000$TolxzjlHKCXEeI/xntP6Xw$k3B9bkXWPzO20/K6T2mqp4XTq9IPoZX2LCeRrRt6ft0",
}

ADMIN_USERS = ["admin"]