DEBUG = True
PORT = 8080
SECRET_KEY = "secret"
WTF_CSRF_ENABLED = True

PASSWORDS = {
    "admin": "$pbkdf2-sha256$29000$GGMM4XxvjVGKsfZ.r5Uypg$IoNQM/K7Sg7YkBew8Ql412RBBjOiiP9FG2rH8dsZ6X4",
}

ADMIN_USERS = ["admin"]