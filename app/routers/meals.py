from typing import List, Optional
from app import models, schema, oauth2
from ..database import get_db, engine
from fastapi import APIRouter, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session



router = APIRouter(
    prefix='/meals',
    tags=['Meals']
)


@router.get("/", response_model=List[schema.Meal])
async def get_meals(db: Session = Depends(get_db), search: Optional[str] = ''):
    meals = db.query(models.Meal).filter(models.Meal.name.contains(search)).all()

    return meals


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schema.Meal)
async def create_meal(data: schema.MealCreate, db: Session = Depends(get_db),
                      user: int = Depends(oauth2.get_current_user)):
    if not user.first().is_staff:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='You are not staff')
    new_meal = models.Meal(**data.dict())
    db.add(new_meal)
    db.commit()
    db.refresh(new_meal)
    return new_meal


@router.get('/{id}', response_model=schema.Meal)
async def get_meal(id: int, db: Session = Depends(get_db)):
    meal = db.query(models.Meal).filter(models.Meal.id == id).first()

    if not meal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No such id')
    return meal


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_meal(id: int, db: Session = Depends(get_db), user: int = Depends(oauth2.get_current_user)):
    meal = db.query(models.Meal).filter(models.Meal.id == id)
    if not meal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No such id')
    if not user.first().is_staff:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='You are not staff')
    meal.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id}', response_model=schema.Meal)
async def update_meal(id: int, updated_meal: schema.MealCreate, db: Session = Depends(get_db),
                      user: int = Depends(oauth2.get_current_user)):
    meal_query = db.query(models.Meal).filter(models.Meal.id == id)
    meal = meal_query.first()
    if not meal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No such id')
    if not user.first().is_staff:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='You are not staff')
    meal_query.update(updated_meal.dict(), synchronize_session=False)
    db.commit()
    return meal_query.first()


@router.get('/category/{category_slug}', response_model=List[schema.Meal])
async def get_meal(category_slug: str, db: Session = Depends(get_db)):
    category = db.query(models.Category).filter(models.Category.slug == category_slug).first()

    meal = db.query(models.Meal).filter(models.Meal.category_id == category.id).all()

    if not meal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No such category')
    return meal
