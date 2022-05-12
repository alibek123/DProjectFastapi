from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, nullable=False, unique=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=False), nullable=False, server_default=text('now()'))
    phone = Column(String(11), nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    is_staff = Column(Boolean, nullable=False, server_default='False')


class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    slug = Column(String, nullable=False)

    # meals = relationship('Meal', back_populates='category')


class Meal(Base):
    __tablename__ = 'meals'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    slug = Column(String, nullable=False, server_default='')  # models.SlugField(default='')
    price = Column(Integer, nullable=False)
    protein = Column(Integer, server_default='0', nullable=False)  # белки
    fats = Column(Integer, server_default='0', nullable=False)  # жиры
    carbs = Column(Integer, server_default='0', nullable=False)  # углеводы
    description = Column(String, nullable=True)
    available_inventory = Column(Integer, server_default='0', nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id', ondelete="CASCADE"), nullable=False)
    # category = relationship("Category", back_populates="meals")
