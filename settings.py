DEBUG = True
PORT = 8080
SECRET_KEY = "secret"
WTF_CSRF_ENABLED = True

PASSWORDS = {
    "admin": "$pbkdf2-sha256$29000$TolxzjlHKCXEeI/xntP6Xw$k3B9bkXWPzO20/K6T2mqp4XTq9IPoZX2LCeRrRt6ft0",
}

ADMIN_USERS = ["admin"]

DATABASE="postgres://ypktmwhlgmijvt:e9d6168a00144a774b298b917a30f946d706365a0379c54da413f6f469b99674@ec2-34-248-148-63.eu-west-1.compute.amazonaws.com:5432/d27qbfil3ivm83"

