from typing import List

from app import models
from fastapi import HTTPException, status


async def initiate_order(user, db) -> models.Order:
    user_info = user.first()
    cart = db.query(models.Cart).filter(models.Cart.user_id == user_info.id).first()

    cart_items_objects = db.query(models.CartItems).join(models.Cart).filter(models.Cart.id == cart.id)

    if not cart_items_objects.count():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No items in cart")

    total_amount = 0.0

    for item in cart_items_objects:
        total_amount += (item.meals.price * item.quantity)

    if total_amount > user_info.balance:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough money")

    user_info.balance -= total_amount
    new_order = models.Order(order_amount=total_amount,
                             customer_id=user_info.id,
                             order_status='COMPLETED')
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    bulk_order_details_obj = list()

    for item in cart_items_objects:
        new_order_detail = models.OrderDetails(order_id=new_order.id,
                                               product_id=item.meals.id)
        bulk_order_details_obj.append(new_order_detail)
    db.bulk_save_objects(bulk_order_details_obj)
    db.commit()

    db.query(models.CartItems).filter(models.CartItems.cart_id == cart.id).delete()
    db.commit()

    return new_order
