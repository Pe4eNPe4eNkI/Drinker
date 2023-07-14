import os
import sys
from random import randrange
from typing import List

from flask import Flask, jsonify, request

from const import FILENAME_DB, StatusOrder
from data import db_session
from data.db_session import Session
from data.models import *


class Main:
    app = Flask(__name__)

    @staticmethod
    def generate_id():  # placeholder
        return randrange(1_000_000_000_000_000)

    @staticmethod
    @app.route('/auth', methods=['GET'])
    def auth():
        """
        ---- ---- JSON
        ---- GET
        :param: {
            login: str
            password: str
        }
        :return: {
            status: ok | fail,
            message: str,
            account_id: int
        }
        """
        login = request.json["login"]
        password = request.json["password"]

        with db_session.create_session() as session:
            acc: Account = session.query(Account).filter(Account.login == login, Account.password == password).first()
            if not acc:
                return jsonify(status="fail", message="incorrect login or password"), 403
            return jsonify(status="ok", message="successful login", account_id=acc.id), 202

    @staticmethod
    @app.route('/register', methods=['PUT'])
    def register():
        """
        ---- ---- JSON
        ---- PUT
        :param: {
            login: str
            password: str
        }
        :return: {
            status: ok | fail,
            message: str,
            account_id: int
        }
        """
        login = request.json["login"]
        password = request.json["password"]

        with db_session.create_session() as session:
            session: Session

            if session.query(Account).filter(Account.login == login).first():
                return jsonify(status="fail", message="a user with such already exists"), 400

            new_cart = CartDetails(id=Main.generate_id())
            new_account = Account(id=Main.generate_id(), login=login, password=password)
            new_user = User(account_id=new_account.id, cart_id=new_cart.id)
            new_info = AccountInfo(account_id=new_account.id)

            session.add_all([new_account, new_user, new_info, new_cart])
            session.commit()
            return jsonify(status="ok", message="User registered successfully", account_id=new_account.id)

    @staticmethod
    @app.route('/account', methods=['POST', 'DELETE'])
    def account():
        """
        ---- ---- JSON
        ---- POST

        changes password and or login of account

        :param: {
            account_Id: int
            login: str
            password: str
        }
        :return: {
            status: ok | fail,
            message: str,
        }

        ---- DELETE

        deletes account of user and all records associeted with it

        :param: {
            account_Id: int
        }
        :return: {
            status: ok | fail,
            message: str,
        }
        """
        with db_session.create_session() as session:
            session: Session

            account_id: int = request.json["account_id"]
            acc: Account = session.query(Account).filter(Account.id == account_id).first()
            if not acc:
                return jsonify(status="fail", message=f"Not found account with id {account_id}"), 404

            if request.method == 'POST':
                login: str = request.json.get("login", None)
                password: str = request.json.get("password", None)
                if login:
                    if not session.query(Account).filter(Account.login == login).first():
                        acc.login = login
                    else:
                        return jsonify(status="fail", message="login already exists"), 409
                if password:
                    acc.password = password
                session.commit()
                return jsonify(status="ok", message="Changed"), 202

            if request.method == "DELETE":
                usr = session.query(User).filter(User.account_id == account_id).first()
                adm = session.query(Admin).filter(Admin.account_id == account_id).first()
                crr = session.query(Courier).filter(Courier.account_id == account_id).first()
                if usr:
                    session.delete(usr)
                if adm:
                    session.delete(adm)
                if crr:
                    session.delete(crr)
                session.delete(acc)
                session.commit()
                return jsonify(status="ok", message="Deleted"), 202

    @staticmethod
    @app.route('/account/info', methods=['GET', 'POST'])
    def account_info():
        """
        ---- ---- JSON
        ---- GET

        :param: {
            account_Id: int
        }
        :return: {
            status: ok | fail,
            message: str,
            login: str,
            name: str,
            middlename: str,
            surname: str,
            phone: str

        }
        ---- POST

        :param: {
            account_Id: int
            name: str,
            middlename: str,
            surname: str,
            phone: str
        }
        :return: {
            status: ok | fail,
            message: str

        }
        """
        with db_session.create_session() as session:
            session: Session

            account_id: int = request.json["account_id"]
            acc: Account = session.query(Account).filter(Account.id == account_id).first()
            if not acc:
                return jsonify(status="fail", message=f"Account with id{account_id} does not exit"), 410

            acc_info: AccountInfo = session.query(AccountInfo).filter(AccountInfo.account_id == account_id).first()
            if request.method == 'GET':
                return jsonify(status="ok", message="Account found", login=acc.login, name=acc_info.name,
                               middlename=acc_info.middlename,
                               surname=acc_info.surname, phone=acc_info.phone)
            if request.method == 'POST':
                acc_name = request.json["name"]
                acc_surname = request.json["surname"]
                acc_middlename = request.json["middlename"]
                acc_phone = request.json["phone"]
                if acc_name:
                    acc_info.name = acc_name
                if acc_surname:
                    acc_info.surname = acc_surname
                if acc_middlename:
                    acc_info.middlename = acc_middlename
                if acc_phone:
                    acc_info.phone = acc_phone
                session.commit()
                return jsonify(status="ok", message=f"Account {account_id} details were changed successfully"), 202

    @staticmethod
    @app.route('/user', methods=['GET', 'POST'])
    def user():
        """
        ---- ---- JSON
        ---- GET
        :param: {
            user_id
        }
        :return: {
            status: ok|fail
            message: str
            user={
                cards= [{
                    number: str
                    names: str
                    date: str
                    cvi: str
                }],
                passport={
                    serial: int
                    number: int
                },
                birth: str,
                verified: bool,
                cart_id: int,
            }
        }
        """
        user_id = request.json['user_id']

        with db_session.create_session() as session:
            session: Session

            usr: User = session.query(User).filter(User.account_id == user_id).first()
            if not usr:
                return jsonify(status="fail", message=f"Not found user with id {user_id}"), 404
            if request.method == "GET":
                cards: List[Card] = list(
                    map(lambda x: x.card_number, session.query(Card).filter(Card.user_id == user_id).all()))
                cards_details: List[CardDetails] = session.query(CardDetails).filter(
                    CardDetails.number.in_(cards)).all()
                cards_data = list(
                    map(lambda x: {"number": x.number, "names": x.names, "date": x.date, "cvi": x.cvi}, cards_details))
                passport: str = None if not usr.passport else usr.passport
                if passport is not None:
                    serial, number = list(map(int, passport.split()))
                    passport_data = {"serial": serial, "number": number}
                else:
                    passport_data = None

                return jsonify(status="ok", message="Founded user", user={
                    "cards": cards_data,
                    "passport": passport_data,
                    "birth": usr.birth,
                    "verified": usr.verified,
                    "cart_id": usr.cart_id,
                }), 202
            if request.method == "POST":
                if 'passport' in request.json:
                    passport: dict = request.json["passport"]
                    usr.passport = f"{passport['serial']} {passport['number']}"
                if 'verified' in request.json:
                    usr.verified = request.json['verified']
                if 'birth' in request.json:
                    usr.birth = request.json['birth']
                session.commit()
                return jsonify(status="ok", message="Changed"), 202

    @staticmethod
    @app.route('/user/card', methods=['PUT', 'DELETE'])
    def user_card():
        """
        ---- ---- JSON
        ---- PUT
        :param: {
            user_id: int
            card= {
                serial: int
                number: int
                names: str
                cvi: int
            }
        }
        :return: {
            status: ok|fail
            message: str
        }
        ---- DELETE
        :param: {
            user_id: int
            card= {
                number: int
            }
        }
        :return: {
            status: ok|fail
            message: str
        }

        """
        user_id = request.json['user_id']

        with db_session.create_session() as session:
            session: Session

            usr: User = session.query(User).filter(User.account_id == user_id).first()
            if not usr:
                return jsonify(status="fail", message=f"Not found user with id {user_id}"), 404

            if request.method == 'PUT':
                card = request.json['card']
                number = card['number']
                if not session.query(CardDetails).filter(CardDetails.number == number).first():
                    names, date, cvi = card['names'], card['date'], card['cvi']
                    card_details = CardDetails(number=number, names=names, date=date, cvi=cvi)
                    session.add(card_details)
                if session.query(Card).filter(Card.user_id == user_id, Card.card_number == number).first():
                    return jsonify(status="fail", message="card exists in user"), 400
                card = Card(user_id=user_id, card_number=number)
                session.add(card)
                session.commit()
                return jsonify(status="ok", message="Card added"), 202
            if request.method == 'DELETE':
                card_number = request.json['card']['number']
                card = session.query(Card).filter(Card.user_id == user_id, Card.card_number == card_number).first()
                if not card:
                    return jsonify(status='fail', message='Not found card in user'), 404
                session.delete(card)
                session.commit()
                return jsonify(status='ok', message='Deleted'), 202

    @staticmethod
    @app.route('/user/cart', methods=['GET', 'POST'])
    def user_cart():
        """
        ---- ---- JSON
        ---- GET
        :param: {
            cart_id: int
        {
        :return: {
            status: ok|fail
            message: str
            items=[{
                cart_id: int
                item_id: int
                count_items: int
            }]
        }
        ---- POST
        // adds to cart count item; by default cart has 0 of any items
        :param: {
            cart_id
            item_id: int
            count: int
        }
        :return: {
            status: ok|fail
            message: str
        }
        """
        with db_session.create_session() as session:
            session: Session

            cart_id: int = request.json["cart_id"]
            if request.method == "GET":
                items_in_cart: List[Cart] = session.query(Cart).filter(Cart.cart_id == cart_id).all()
                json_of_items_in_cart = []
                for entry in items_in_cart:
                    json_of_items_in_cart.append(
                        {"cart_id": entry.cart_id, "item_id": entry.item_id, "count_items": entry.count_items})
                return jsonify(status="ok", message="Fetched successfully", items=json_of_items_in_cart)

            if request.method == "POST":
                new_item = request.json["item_id"]
                new_item_count = request.json["count"]

                if new_item is None:
                    return jsonify(status="fail", message="Item ID is missing"), 400
                if new_item_count is None:
                    new_item_count = 1
                in_cart = session.query(Cart).filter(Cart.item_id == new_item).first()
                if in_cart is None:
                    # item is new
                    new_cart = Cart(cart_id=cart_id, item_id=new_item, count_items=new_item_count)
                    session.add(new_cart)
                    session.commit()
                    return jsonify(status="ok", message="Added Successfully"), 202
                # for old items we just change count
                old_count = in_cart.count_items
                in_cart.count_items = new_item_count + old_count
                session.commit()
                return jsonify(status="ok", message=f"Items added successfully; now {old_count + new_item_count}"), 202

    @staticmethod
    @app.route('/order', methods=['GET'])
    def order():
        """
        ---- ---- JSON
        ---- GET
        :param: {
            order_id: int
        }
        :return: {
            status: ok|fail
            message: str
            order={
                order_id: int
                user_id: int
                courier_id: int
                address: str
                status: enum
                cart_id: int
            }
        }
        """
        order_id = request.json['order_id']
        with db_session.create_session() as session:
            session: Session

            order_ = session.query(Order).filter(Order.order_id == order_id).first()
            order_details = session.query(OrderDetails).filter(OrderDetails.id == order_id).first()
            if order_ is None:
                return jsonify(status="fail", message=f"Order number {order_id} does not exist")
            order_info = jsonify(
                order_id=order_id,
                user_id=order_.user_id,
                courier_id=order_.courier_id,
                address=order_details.id,
                status=order_details.status,
                cart_id=order_details.cart_id
            )
            return jsonify(status="ok", message="order found", order=order_info)

    @staticmethod
    @app.route('/order/make', methods=['PUT'])
    def make_order():
        user_id = request.json['user_id']
        address = request.json['address']
        with db_session.create_session() as session:
            session: Session
            usr: Cart = session.query(User).filter(User.account_id == user_id).first()
            if not usr:
                return jsonify(status="fail", message=f"Not found user with id: {user_id}"), 404
            order_details = OrderDetails(id=randrange(1 << 16), cart_id=usr.cart_id, address=address)
            order_ = Order(order_id=order_details.id, user_id=user_id, courier_id=None)

            cart = CartDetails(randrange(1 << 16))
            usr.cart_id = cart.id
            session.add_all([order_details, order_, cart])
            session.commit()
            return jsonify(status="ok", message="created order", order_id=order_details.id), 202

    @staticmethod
    @app.route('/order/free', methods=['GET'])
    def free_orders():
        """
        ---- ---- JSON
        ---- GET
        :param: {}
        :return: {
            status: ok | fail,
            message: str,
            orders=[
                {
                    id: int,
                    cart_id: int,
                    address: str,
                    status: enum
                }
            ]
        }
        """

        with db_session.create_session() as session:
            session: Session

            orders: List[Order] = session.query(Order).filter(Order.courier_id.is_(None))
            order_ids = list(map(lambda x: x.order_id, orders))
            order_details: List[OrderDetails] = session.query(OrderDetails).filter(OrderDetails.id.in_(order_ids)).all()
            order_data = [{"id": x.id, "cart_id": x.cart_id, "address": x.address, "status": x.status} for x in
                          order_details]
            return jsonify(status="ok", message="free orders", orders=order_data), 202

    @staticmethod
    @app.route('/order/accept', methods=['POST'])
    def order_accept():
        """
        ---- ---- JSON
        ---- POST
        :param: {
            order_id: int
            courier_id: int
        }
        :return: {
            status: ok|fail,
            message: str
        }
        """

        order_id = request.json['order_id']
        courier_id = request.json['courier_id']
        with db_session.create_session() as session:
            session: Session

            order_: Order = session.query(Order).filter(Order.order_id == order_id).first()
            if not session.query(Courier).filter(Courier.account_id == courier_id):
                return jsonify(status="fail", message=f"Not found courier with id: {courier_id}"), 404
            order_.courier_id = courier_id
            order_details: OrderDetails = session.query(OrderDetails).filter(OrderDetails.id == order_id).first()
            order_details.status = StatusOrder.ON_WAY
            session.commit()
            return jsonify(status="ok", message=f"Accepted order")

    @staticmethod
    @app.route('/order/done', methods=['POST'])
    def order_done():
        """
        ---- ---- JSON
        ---- POST
        :param: {
            order_id: int
        }
        :return: {
            status: ok|fail,
            message: str
        }
        """

        order_id = request.json['order_id']
        with db_session.create_session() as session:
            session: Session

            order_details: OrderDetails = session.query(OrderDetails).filter(
                OrderDetails.id == order_id, OrderDetails.status != StatusOrder.DONE).first()
            if not order_details:
                return jsonify(status="fail", message=f"Not found order with id: {order_id}"), 404
            order_details.status = StatusOrder.DONE
            session.commit()
            return jsonify(status="ok", message=f"Order is done")

    @staticmethod
    @app.route('/order/fail', methods=['POST'])
    def order_fail():
        """
        ---- ---- JSON
        ---- POST
        :param: {
            order_id: int
        }
        :return: {
            status: ok|fail,
            message: str
        }
        """

        order_id = request.json['order_id']
        with db_session.create_session() as session:
            session: Session

            order_details: OrderDetails = session.query(OrderDetails).filter(OrderDetails.id == order_id).first()
            if not order_details:
                return jsonify(status="fail", message=f"Not found order with id: {order_id}"), 404
            order_details.status = StatusOrder.FAILED
            session.commit()
            return jsonify(status="ok", message=f"Order is fail")

    @staticmethod
    @app.route('/order/user', methods=['GET'])
    def find_user_orders():
        """
        ---- ---- JSON
        ---- GET
        :param: {
            user_id: int
        }
        :return: {
            status: ok|fail,
            message: str,
            orders=[
                {
                    id: int,
                    cart_id: int,
                    address: str,
                    status: enum
                }
            ]
        }
        """

        user_id = request.json['user_id']
        with db_session.create_session() as session:
            session: Session

            order_ids: List[int] = list(
                map(lambda x: x.order_id, session.query(Order).filter(Order.user_id == user_id).all()))
            orders: List[OrderDetails] = session.query(OrderDetails).filter(OrderDetails.id.in_(order_ids)).all()
            order_data = [{"id": x.id, "cart_id": x.cart_id, "address": x.address, "status": x.status} for x in
                          orders]
            return jsonify(status="ok", message="user orders", orders=order_data)

    @staticmethod
    @app.route('/order/courier', methods=['GET'])
    def find_courier_orders():
        """
        ---- ---- JSON
        ---- GET
        :param: {
            courier_id: int
        }
        :return: {
            status: ok|fail,
            message: str,
            orders=[
                {
                    id: int,
                    cart_id: int,
                    address: str,
                    status: enum
                }
            ]
        }
        """

        courier_id = request.json['courier_id']
        with db_session.create_session() as session:
            session: Session

            order_ids: List[int] = list(
                map(lambda x: x.order_id, session.query(Order).filter(Order.courier_id == courier_id).all()))
            orders: List[OrderDetails] = session.query(OrderDetails).filter(OrderDetails.id.in_(order_ids)).all()
            order_data = [{"id": x.id, "cart_id": x.cart_id, "address": x.address, "status": x.status} for x in
                          orders]
            return jsonify(status="ok", message="courier orders", orders=order_data)

    @staticmethod
    @app.route('/tags', methods=['GET'])
    def tags():
        """
        ---- ---- JSON
        ---- GET
        :param: {}
        :return: {
            status: ok|fail,
            message: str,
            tags=[
                {
                    id: int,
                    name: str
                }
            ]
        }
        """

        with db_session.create_session() as session:
            session: Session
            tags_: List[Tag] = session.query(Tag).all()
            tags_json = [{"id": tag.id, "name": tag.name} for tag in tags_]
            return jsonify(status="ok", message="get all items", tags=tags_json), 202

    @staticmethod
    @app.route('/items', methods=['GET', 'PUT', 'POST', 'DELETE'])
    def items():
        """
        ---- ---- JSON
        ---- GET
        :param: {
            item_id: int
        }
        :return: {
            status: ok|fail,
            message: str,
            item={
                id: int,
                name: str,
                price: float,
                image_url: str,
                desc: str,
                tag={
                    id: int,
                    name: str
                }
            }
        }

        ---- ---- JSON
        ---- PUT
        :param: {
            name: str,
            price: float,
            image_url: str,
            desc: str,
            tag_id: int

        }
        :return: {
            status: ok|fail,
            message: str,
            item_id: int
        }

        ---- ---- JSON
        ---- POST
        :param: {
            item_id: int,
            name: str,
            price: float,
            image_url: str,
            desc: str,
            tag_id: int

        }
        :return: {
            status: ok|fail,
            message: str
        }

        ---- ---- JSON
        ---- DELETE
        :param: {
            item_id: int
        }
        :return: {
            status: ok|fail,
            message: str
        }
        """
        with db_session.create_session() as session:
            session: Session
            if request.method == 'GET':
                item_id = request.json['item_id']
                item: Item = session.query(Item).filter(Item.id == item_id).first()
                if not item:
                    return jsonify(status='fail', message=f'Not found item with id: {item_id}'), 404
                if item.tag_id:
                    t: Tag = session.query(Tag).filter(Tag.id == item.tag_id)
                    tag = {"id": t.id, "name": t.name}
                else:
                    tag = None
                return jsonify(status="ok", message="get item", item={
                    "id": item.id, "name": item.name, "price": item.price,
                    "image_url": item.image_url, "desc": item.desc, "tag": tag})
            if request.method == "PUT":
                item_id = randrange(1 << 16)
                item_name = request.json['name']
                item_price = request.json['price']
                item_image_url = request.json.get('image_url')
                item_desc = request.json.get('desc')
                item_tag = request.json.get('tag_id')
                if item_tag is not None and not session.query(Tag).filter(Tag.id == item_tag).first():
                    return jsonify(status="fail", message=f"Not found tag with id: {item_tag}")
                item = Item(id=item_id, name=item_name, price=item_price, image_uml=item_image_url, desc=item_desc,
                            tag_id=item_tag)
                session.add(item)
                session.commit()
                return jsonify(status="ok", message="Item added", item_id=item_id)
            if request.method == 'POST':
                item_id = request.json['item_id']
                item: Item = session.query(Item).filter(Item.id == item_id).first()
                if 'name' in request.json:
                    item.name = request.json['name']
                if 'price' in request.json:
                    item.price = request.json['price']
                if 'image_uml' in request.json:
                    item.image_uml = request.json['image_uml']
                if 'desc' in request.json:
                    item.desc = request.json['desc']
                if 'tag' in request.json:
                    tag_id = request.json['tag_id']
                    if tag_id is not None and not session.query(Tag).filter(Tag.id == tag_id).first():
                        return jsonify(status="fail", message=f"Not found tag with id: {tag_id}")
                    item.tag = request.json['tag']
                session.commit()
                return jsonify(status="ok", message="Changed"), 202
            if request.method == 'DELETE':
                item_id = request.json['item_id']
                for elem in session.query(Cart).filter(Cart.item_id == item_id).all():
                    session.delete(elem)
                item: Item = session.query(Item).filter(Item.id == item_id).first()
                if not item:
                    return jsonify(status="fail", message=f"Not found item with id: {item_id}"), 404
                session.delete(item)
                session.commit()
                return jsonify(status="ok", message="Deleted"), 202

    @staticmethod
    @app.route('/gallery', methods=['GET'])
    def gallery():
        """
        ---- ---- JSON
        ---- GET
        :param: {}
        :return: {
            status: ok|fail,
            message: str,
            items=[
                {
                    id: int,
                    name: str,
                    price: float,
                    image_url: str
                    desc: str
                    tag={
                        id: int,
                        name: str
                    }
                }
            ]
        }
        """

        with db_session.create_session() as session:
            session: Session
            items_: List[Item] = session.query(Item).all()
            items_json = [{
                "id": item.id, "name": item.name, "price": item.price, "image_url": item.image_url, "desc": item.desc,
                "tag": {"id": item.tag_id, "name": session.query(Tag).filter(Tag.id == item.tag_id).first().name}
            } for item in items_]

            return jsonify(status="ok", message="get all items", items=items_json), 202

    @staticmethod
    def main():
        if '--reset' in sys.argv:
            if os.path.isfile(FILENAME_DB):
                os.remove(FILENAME_DB)
        db_session.global_init(FILENAME_DB)
        if '--reset' in sys.argv:
            with db_session.create_session() as session:
                pass

        Main.app.run(host="127.0.0.1", port=5000)


if __name__ == "__main__":
    Main.main()
