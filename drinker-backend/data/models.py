from .db_session import SqlAlchemyBase, Session
from sqlalchemy import ForeignKey, Column, String, Integer, Float, Boolean, Date


class Account(SqlAlchemyBase):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True, autoincrement=True)

    login = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)

    @staticmethod
    def get(session: Session, *, id: int) -> "Account":
        return session.query(Account).filter(Account.id == id).first()

    def to_json(self) -> dict:
        return {"id": self.id, "login": self.login}


class AccountInfo(SqlAlchemyBase):
    __tablename__ = "accounts_info"

    account_id = Column(Integer, ForeignKey('accounts.id'), primary_key=True)

    name = Column(String)
    surname = Column(String)
    middlename = Column(String)
    phone = Column(String)

    @staticmethod
    def get(session: Session, *, account_id: int) -> "AccountInfo":
        return session.query(AccountInfo).filter(AccountInfo.account_id == account_id).first()


class User(SqlAlchemyBase):
    __tablename__ = "users"

    account_id = Column(Integer, ForeignKey('accounts.id'), primary_key=True)
    passport = Column(String)
    birth = Column(String)
    cart_id = Column(Integer, ForeignKey('cart_details.id'), nullable=False)

    @staticmethod
    def get(session: Session, *, account_id: int) -> "User":
        return session.query(User).filter(User.account_id == account_id).first()


class Admin(SqlAlchemyBase):
    __tablename__ = "admins"

    account_id = Column(Integer, ForeignKey('accounts.id'), primary_key=True)

    @staticmethod
    def get(session: Session, *, account_id: int) -> "Admin":
        return session.query(Admin).filter(Admin.account_id == account_id).first()


class Courier(SqlAlchemyBase):
    __tablename__ = "couriers"

    account_id = Column(Integer, primary_key=True, autoincrement=True)

    @staticmethod
    def get(session: Session, *, account_id: int) -> "Courier":
        return session.query(Courier).filter(Courier.account_id == account_id).first()


class CardDetails(SqlAlchemyBase):
    __tablename__ = "card_details"
    number = Column(String, primary_key=True)

    names = Column(String, nullable=False)
    date = Column(String, nullable=False)
    cvi = Column(String, nullable=False)

    @staticmethod
    def get(session: Session, *, number: str) -> "CardDetails":
        return session.query(CardDetails).filter(CardDetails.number == number).first()


class Card(SqlAlchemyBase):
    __tablename__ = "cards"

    user_id = Column(Integer, ForeignKey('users.account_id'), primary_key=True)
    card_number = Column(String, ForeignKey('card_details.number'), primary_key=True)

    @staticmethod
    def get(session: Session, *, user_id: int) -> "Card":
        return session.query(Card).filter(Card.user_id == user_id).first()


class CartDetails(SqlAlchemyBase):
    __tablename__ = "cart_details"

    id = Column(Integer, primary_key=True)

    @staticmethod
    def get(session: Session, *, id: int) -> "CardDetails":
        return session.query(CardDetails).filter(CardDetails.id == id).first()


class Cart(SqlAlchemyBase):
    __tablename__ = "carts"

    cart_id = Column(Integer, ForeignKey('cart_details.id'), primary_key=True)
    item_id = Column(Integer, ForeignKey('items.id'), primary_key=True)
    count_items = Column(Integer, nullable=False, default=1)

    @staticmethod
    def get(session: Session, *, cart_id: int, item_id: int) -> "Cart":
        return session.query(Cart).filter(Cart.cart_id == cart_id, Cart.item_id == item_id).first()


class Order(SqlAlchemyBase):
    __tablename__ = "orders"

    order_id = Column(Integer, ForeignKey('order_details.id'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.account_id'), nullable=False)
    courier_id = Column(Integer, ForeignKey('couriers.account_id'))

    @staticmethod
    def get(session: Session, *, order_id: int) -> "Order":
        return session.query(Cart).filter(Order.order_id == order_id).first()


class OrderDetails(SqlAlchemyBase):
    __tablename__ = "order_details"

    id = Column(Integer, primary_key=True, autoincrement=True)

    cart_id = Column(Integer, ForeignKey('cart_details.id'), nullable=False, unique=True)
    address = Column(String, nullable=False)
    status = Column(Integer, nullable=False, default=0)

    @staticmethod
    def get(session: Session, *, id: int) -> "OrderDetails":
        return session.query(Cart).filter(OrderDetails.id == id).first()


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

