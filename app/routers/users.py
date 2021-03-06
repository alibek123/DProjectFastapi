from app import oauth2
from app.database import get_db
from sqlalchemy.orm import Session
from typing import Optional

from .. import schema, utils, models
from fastapi import status, HTTPException, APIRouter, Depends

router = APIRouter(
    prefix='/users',
    tags=['User']
)


@router.get('/', response_model=schema.User)
async def get_user(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    user = current_user.first()
    return user


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schema.User)
async def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    # hash password
    hashed_pass = utils.hash(user.password)
    user.password = hashed_pass
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/{id}', response_model=schema.User)
async def get_user(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    if (id != current_user.first().id) and (not current_user.first().is_staff):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='You can only view your information')

    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No such user with this id')
    return user


@router.put('/balance', status_code=status.HTTP_201_CREATED, response_model=schema.User)
async def update_user_balance(data: schema.Update_Balance, db: Session = Depends(get_db),
                              # phone: str = '', balance: int = 0,
                              current_user: int = Depends(oauth2.get_current_user)):
    phone = data.dict()['phone']
    balance = data.dict()['balance']

    if (id != current_user.first().id) and (not current_user.first().is_staff):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Only staff')
    user = db.query(models.User).filter(models.User.phone == phone).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No such user with this phone')
    user.balance += balance
    db.commit()
    return user
