from typing import List

from app.database import get_db
from app.routers import services
from fastapi import APIRouter, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
from app import schema, models, oauth2

router = APIRouter(
    prefix='/orders',
    tags=['Orders']
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schema.ShowOrder)
async def initiate_order_processing(db: Session = Depends(get_db),
                                    user: int = Depends(oauth2.get_current_user)):
    res = await services.initiate_order(user, db)
    return res


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[schema.ShowOrder])
async def orders_list(db: Session = Depends(get_db),
                      user: int = Depends(oauth2.get_current_user)):
    user_info = user.first()
    orders = db.query(models.Order).filter(models.Order.customer_id == user_info.id).all()
    return orders
