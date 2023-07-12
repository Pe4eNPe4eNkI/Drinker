from db_session import SqlAlchemyBase, orm
from sqlalchemy import ForeignKey, Column, String, Integer, Float, Boolean


class Account(SqlAlchemyBase):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    login = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    cards = Column(String, nullable=False, default="")
    verified = Column(Boolean, nullable=False, default=False)

    orders = orm.relation('Order', back_populates='account_id')


class AccountInfo(SqlAlchemyBase):
    __tablename__ = "accounts_info"

    account_id = Column(Integer, ForeignKey('accounts.id'), primary_key=True)

    name = Column(String)
    surname = Column(String)
    middlename = Column(String)
    phone = Column(String)


class Card(SqlAlchemyBase):
    __tablename__ = "cards"

    number = Column(String, primary_key=True)
    names = Column(String, nullable=False)
    date = Column(String, nullable=False)
    cvi = Column(String, nullable=False)


class Cart(SqlAlchemyBase):
    __tablename__ = "carts"
    id = Column(Integer, primary_key=True, autoincrement=True)

    account_id = Column(Integer, ForeignKey('accounts.id'))
    items_ids = Column(String, nullable=False, default="{}")


class Courier(SqlAlchemyBase):
    __tablename__ = "couriers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    courier_type = Column(String)
    # destination = Column(String)

    orders = orm.relation('Order', back_populates='courier_id')


class Order(SqlAlchemyBase):
    __tablename__ = "orders"

    id = Column(Integer)
    account_id = Column(Integer, ForeignKey('accounts.id'))
    courier_id = Column(Integer, ForeignKey('couriers.id'))
    address = Column(String, nullable=False)
    status = Column(Integer, nullable=False)

    account = orm.relation('Account')
    courier = orm.relation('Courier')


class Gallery(SqlAlchemyBase):
    __tablename__ = "galleries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    items = Column(String, nullable=False, default="[]")


class Item(SqlAlchemyBase):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    desc = Column(String)
