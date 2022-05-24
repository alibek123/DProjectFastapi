from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey, Float
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
    balance = Column(Integer, nullable=False, server_default='0')
    cart = relationship("Cart", back_populates="user_cart")
    order = relationship("Order", back_populates="user_info")


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
    # image = Column(String(), nullable=True)
    # thumbnail = Column(String(), nullable=True)
    cart_items = relationship("CartItems", back_populates="meals")
    order_details = relationship("OrderDetails", back_populates="product_order_details")
    # category = relationship("Category", back_populates="meals")


class Cart(Base):
    __tablename__ = 'cart'
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey(User.id, ondelete="CASCADE"))
    cart_items = relationship("CartItems", back_populates="cart")
    user_cart = relationship("User", back_populates="cart")
    created_at = Column(TIMESTAMP(timezone=False), nullable=False, server_default=text('now()'))


class CartItems(Base):
    __tablename__ = 'cart_items'
    id = Column(Integer, primary_key=True, nullable=False)
    cart_id = Column(Integer, ForeignKey("cart.id", ondelete="CASCADE"))
    product_id = Column(Integer, ForeignKey(Meal.id, ondelete="CASCADE"))
    cart = relationship("Cart", back_populates="cart_items")
    meals = relationship("Meal", back_populates="cart_items")
    created_at = Column(TIMESTAMP(timezone=False), nullable=False, server_default=text('now()'))


#
class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, nullable=False)
    order_amount = Column(Float, default=0.0)
    order_status = Column(String, default="PROCESSING")
    order_date = Column(TIMESTAMP(timezone=False), nullable=False, server_default=text('now()'))
    customer_id = Column(Integer, ForeignKey(User.id, ondelete="CASCADE"), nullable=False)
    order_details = relationship("OrderDetails", back_populates="order")
    user_info = relationship("User", back_populates="order")


class OrderDetails(Base):
    __tablename__ = "order_details"

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('orders.id', ondelete="CASCADE"), )
    product_id = Column(Integer, ForeignKey(Meal.id, ondelete="CASCADE"), )
    order = relationship("Order", back_populates="order_details")
    product_order_details = relationship("Meal", back_populates="order_details")
    quantity = Column(Integer, default=1)
    created_at = Column(TIMESTAMP(timezone=False), nullable=False, server_default=text('now()'))
