from .. import schema, models, utils, oauth2
from ..database import get_db
from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

router = APIRouter(tags=['Authentication'])


@router.post('/login',response_model=schema.Token)
def login(user_creds: schema.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_creds.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Неправильные данные")

    if not utils.verify(user_creds.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Неправильные данные")

    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}
