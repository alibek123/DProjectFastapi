from app import models
from app.database import get_db
from fastapi import Depends, status, HTTPException
from jose import JWTError, jwt
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from . import schema, database
from fastapi.security import OAuth2PasswordBearer

ouath2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = "610c0e7d0003d7e01905f45ce41be5ea32aa4676e6e0f6558f2e76e2c2413ea8"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return token


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, [ALGORITHM])
        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception
        token_data = schema.TokenData(id=id)
    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(token: str = Depends(ouath2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Авторизуйтесь',
                                          headers={"WWW-Authenticate": "Bearer"})
    token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id)
    return user
