from app.database import get_db
from fastapi import APIRouter, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
from app import schema, models, oauth2

router = APIRouter(
    prefix='/cart',
    tags=['Cart']
)


async def add_items(cart_id, meal_id, quantity, db: Session = Depends(get_db)):
    existing_cart_item = db.query(models.CartItems).filter(models.CartItems.cart_id == cart_id,
                                                           models.CartItems.product_id == meal_id)
    cart_items = models.CartItems(cart_id=cart_id, product_id=meal_id, quantity=quantity)

    if existing_cart_item.first():
        existing_cart_item.first().quantity += quantity
        db.commit()
    else:
        db.add(cart_items)
        db.commit()
        db.refresh(cart_items)


@router.post('/{product_id}', status_code=status.HTTP_201_CREATED)
async def add_product_to_cart(product_id: int, quantity: int = 1, db: Session = Depends(get_db),
                              user: int = Depends(oauth2.get_current_user)):
    meal_info = db.query(models.Meal).get(product_id)
    user_info = user.first()
    cart_info = db.query(models.Cart).filter(models.Cart.user_id == user_info.id).first()
    print(meal_info)
    if meal_info.available_inventory - quantity < 0:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='Не хватает товара')
    if not cart_info:
        new_cart = models.Cart(user_id=user_info.id)
        db.add(new_cart)
        db.commit()
        db.refresh(new_cart)
        await add_items(new_cart.id, meal_info.id, quantity, db)
    else:
        await add_items(cart_info.id, meal_info.id, quantity, db)
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
    cart_id = db.query(models.Cart).join(models.User).filter(models.User.id == user_info.id).first()

    meal = db.query(models.CartItems).filter(models.CartItems.product_id == product_id,
                                             models.CartItems.cart_id == cart_id.id)

    if meal.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No such meal in your cart')

    meal.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
