from typing import List
from app import models, schema
from ..database import get_db, engine
from fastapi import APIRouter, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session

# models.Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix='/category',
    tags=['Category']
)


@router.get("/", response_model=List[schema.Category])
async def get_categories(db: Session = Depends(get_db)):
    categories = db.query(models.Category).all()
    return categories


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schema.Category)
async def create_category(data: schema.CategoryCreate, db: Session = Depends(get_db)):
    new_category = models.Category(**data.dict())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category
