from .db_session import SqlAlchemyBase
from sqlalchemy import ForeignKey, Column, String, Integer, Float, Boolean, Date


class Account(SqlAlchemyBase):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True, autoincrement=True)

    login = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)


class AccountInfo(SqlAlchemyBase):
    __tablename__ = "accounts_info"

    account_id = Column(Integer, ForeignKey('accounts.id'), primary_key=True)

    name = Column(String)
    surname = Column(String)
    middlename = Column(String)
    phone = Column(String)


class User(SqlAlchemyBase):
    __tablename__ = "users"

    account_id = Column(Integer, ForeignKey('accounts.id'), primary_key=True)
    passport = Column(String)
    birth = Column(String)
    cart_id = Column(Integer, ForeignKey('cart_details.id'), nullable=False)


class Admin(SqlAlchemyBase):
    __tablename__ = "admins"

    account_id = Column(Integer, ForeignKey('accounts.id'), primary_key=True)


class Courier(SqlAlchemyBase):
    __tablename__ = "couriers"

    account_id = Column(Integer, primary_key=True, autoincrement=True)


class CardDetails(SqlAlchemyBase):
    __tablename__ = "card_details"
    number = Column(String, primary_key=True)

    names = Column(String, nullable=False)
    date = Column(String, nullable=False)
    cvi = Column(String, nullable=False)


class Card(SqlAlchemyBase):
    __tablename__ = "cards"

    user_id = Column(Integer, ForeignKey('users.account_id'), primary_key=True)
    card_number = Column(String, ForeignKey('card_details.number'), primary_key=True)


class CartDetails(SqlAlchemyBase):
    __tablename__ = "cart_details"

    id = Column(Integer, primary_key=True)


class Cart(SqlAlchemyBase):
    __tablename__ = "carts"

    cart_id = Column(Integer, ForeignKey('cart_details.id'), primary_key=True)
    item_id = Column(Integer, ForeignKey('items.id'), primary_key=True)
    count_items = Column(Integer, nullable=False, default=1)


class Order(SqlAlchemyBase):
    __tablename__ = "orders"

    order_id = Column(Integer, ForeignKey('order_details.id'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.account_id'), nullable=False)
    courier_id = Column(Integer, ForeignKey('couriers.account_id'))


class OrderDetails(SqlAlchemyBase):
    __tablename__ = "order_details"

    id = Column(Integer, primary_key=True, autoincrement=True)

    cart_id = Column(Integer, ForeignKey('cart_details.id'), nullable=False, unique=True)
    address = Column(String, nullable=False)
    status = Column(Integer, nullable=False, default=0)


class GalleryDetails(SqlAlchemyBase):
    __tablename__ = "gallery_details"

    id = Column(Integer, primary_key=True, autoincrement=True)


class Item(SqlAlchemyBase):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, autoincrement=True)

    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    image_url = Column(String)
    desc = Column(String)
    tag_id = Column(Integer, ForeignKey('tags.id'))


class Tag(SqlAlchemyBase):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)

