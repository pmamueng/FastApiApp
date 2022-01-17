from datetime import datetime, timedelta
from jose import JWTError, jwt


SECRET_KEY = "78a63a0e12f5f8b2e4daacdc7193c6ebb3e75cfa162ded5f8f957f2b9e271d2f"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt