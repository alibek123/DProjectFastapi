from app.database import get_db
from fastapi import APIRouter, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
from app import schema, models, oauth2

router = APIRouter(
    prefix='/cart',
    tags=['Cart']
)


async def add_items(cart_id, meal_id, db: Session = Depends(get_db)):
    cart_items = models.CartItems(cart_id=cart_id, product_id=meal_id)
    db.add(cart_items)
    db.commit()
    db.refresh(cart_items)


@router.post('/{product_id}', status_code=status.HTTP_201_CREATED)
async def add_product_to_cart(product_id: int, db: Session = Depends(get_db),
                              user: int = Depends(oauth2.get_current_user)):
    meal_info = db.query(models.Meal).get(product_id)

    user_info = user.first()
    cart_info = db.query(models.Cart).filter(models.Cart.user_id == user_info.id).first()

    if not cart_info:
        new_cart = models.Cart(user_id=user_info.id)
        db.add(new_cart)
        db.commit()
        db.refresh(new_cart)
        await add_items(new_cart.id, meal_info.id, db)
    else:
        await add_items(cart_info.id, meal_info.id, db)
    return {'status': 'Item added to cart'}


@router.get('/', response_model=schema.ShowCart)
async def get_all_cart_items(db: Session = Depends(get_db),
                             user: int = Depends(oauth2.get_current_user)):
    user_info = user.first()
    cart = db.query(models.Cart).filter(models.Cart.user_id == user_info.id).first()
    if not cart:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No such id')
    return cart


@router.delete('/{product_id}', status_code=status.HTTP_204_NO_CONTENT)
async def remove_cart_item(product_id: int, db: Session = Depends(get_db),
                           user: int = Depends(oauth2.get_current_user)):
    user_info = user.first()
    cart_id = db.query(models.Cart).filter(models.User.id == user_info.id).first()

    meal = db.query(models.CartItems).filter(models.CartItems.id == product_id,
                                             models.CartItems.cart_id == cart_id.id)
    if not meal.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No such meal in your cart')

    meal.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
