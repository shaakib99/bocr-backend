import random, string, hashlib
import jwt
from bocr.settings import SECRET_KEY


def randomStringGenerator(length=22):
    return ''.join(
        random.choices(string.ascii_letters + string.digits, k=length))


def hashPassword(password: str):
    return hashlib.md5(password.encode('utf8')).hexdigest()


def jwtEncode(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm="HS256")


def jwtDecode(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
