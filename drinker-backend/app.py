from flask import Flask, Blueprint, jsonify, request
from typing import List

from data import db_session
from data.db_session import Session
from data.models import *
from const import FILENAME_DB, StatusOrder
from random import randrange

app = Flask(__name__)

bp = Blueprint('api', __name__, url_prefix='/api')
app.register_blueprint(bp)


def generate_id():
    return randrange(1_000_000_000_000_000)


@app.route('/auth', methods=['GET'])
def auth():
    login = request.json["login"]
    password = request.json["password"]

    with db_session.create_session() as session:
        acc: Account = session.query(Account).filter(Account.login == login, Account.password == password).first()
        if not acc:
            return jsonify(status="fail", message="incorrect login or password"), 403
        return jsonify(status="ok", message="successful login", account_id=acc.id), 202


@app.route('/register', methods=['PUT'])
def register():
    login = request.json["login"]
    password = request.json["password"]

    with db_session.create_session() as session:
        session: Session

        if session.query(Account).filter(Account.login == login).first():
            return jsonify(status="fail", message="a user with such already exists"), 400

        new_cart = CartDetails(id=generate_id())
        new_account = Account(id=generate_id(), login=login, password=password)
        new_user = User(account_id=new_account.id, cart_id=new_cart.id)
        new_info = AccountInfo(account_id=new_account.id)

        session.add_all([new_account, new_user, new_info, new_cart])
        session.commit()
        return jsonify(status="ok", message="User registered successfully", account_id=new_account.id)


@app.route('/account', methods=['POST', 'DELETE'])
def account():
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


@app.route('/account/info', methods=['GET', 'POST'])
def account_info():
    with db_session.create_session() as session:
        session: Session

        account_id: int = request.json["account_id"]
        acc: Account = session.query(Account).filter(Account.id == account_id).first()
        if not acc:
            return jsonify(status="fail", message=f"Account with id{account_id} does not exit"), 410

        acc_info: AccountInfo = session.query(AccountInfo).filter(AccountInfo.account_id == account_id).first()
        if request.method == 'GET':
            return jsonify(login=acc.login, name=acc_info.name, middlename=acc_info.middlename,
                           surname=acc_info.surname, phone=acc_info.phone)
        # adds data from json to AccountInfo; AccountInfo is created on registration
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


@app.route('/user', methods=['GET', 'POST'])
def user():
    user_id = request.json['user_id']

    with db_session.create_session() as session:
        session: Session

        usr: User = session.query(User).filter(User.account_id == user_id).first()
        if not usr:
            return jsonify(status="fail", message=f"Not found user with id {user_id}"), 404
        if request.method == "GET":
            cards: List[Card] = list(
                map(lambda x: x.card_number, session.query(Card).filter(Card.user_id == user_id).all()))
            cards_details: List[CardDetails] = session.query(CardDetails).filter(CardDetails.number.in_(cards)).all()
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


@app.route('/user/card', methods=['PUT', 'DELETE'])
def user_card():
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


@app.route('/user/cart', methods=['GET', 'POST'])
def user_cart():
    with db_session.create_session() as session:
        session: Session

        cart_id: int = request.json["cart_id"]
        if request.method == "GET":
            items_in_cart: List[Cart] = session.query(Cart).filter(Cart.cart_id == cart_id).all()
            json_of_items_in_cart = []
            for entry in items_in_cart:
                json_of_items_in_cart.append({"cart_id": entry.cart_id, "count_items": entry.count_items})
            return jsonify(status="ok", message="Fetched successfully", items=json_of_items_in_cart)

        if request.method == "POST":
            new_item = request.json["new_item"]
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


@app.route('/order', methods=['GET'])
def order():
    with db_session.create_session() as session:
        session: Session
        order_id_ = request.json['order_id']
        order_: Order = session.query(Order).filter(Order.order_id == order_id_).first() # TODO: Check
        if not order_:
            return jsonify(status='fail', message=f'Not found item with id: {order_id_}'), 404
        if order_.user_id:
            usr: Order = session.query(Order).filter(Order.id == Order.user_id)
        if order_.courier_id:
            usr: Order = session.query(Order).filter(Order.id == Order.courier_id)
        return jsonify(order_id=order_.order_id, user_id=order_.user_id, courier_id=order_.courier_id)

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


@app.route('/order/free', methods=['GET'])
def free_orders():
    """
    ---- ---- JSON
    ---- GET
    params: {}
    return: {
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


@app.route('/order/accept', methods=['POST'])
def order_accept():
    """

    """

    order_id = request.json['order_id']
    courier_id = request.json['order_id']
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


@app.route('/order/done', methods=['POST'])
def order_done():
    """

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


@app.route('/order/fail', methods=['POST'])
def order_fail():
    """

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


@app.route('/order/user', methods=['GET'])
def find_user_orders():
    """

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


@app.route('/order/courier', methods=['GET'])
def find_courier_orders():
    """

    """

    courier_id = request.json['user_id']
    with db_session.create_session() as session:
        session: Session

        order_ids: List[int] = list(
            map(lambda x: x.order_id, session.query(Order).filter(Order.courier_id == courier_id).all()))
        orders: List[OrderDetails] = session.query(OrderDetails).filter(OrderDetails.id.in_(order_ids)).all()
        order_data = [{"id": x.id, "cart_id": x.cart_id, "address": x.address, "status": x.status} for x in
                      orders]
        return jsonify(status="ok", message="courier orders", orders=order_data)


@app.route('/tags', methods=['GET'])
def tags():
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
            return jsonify(id=item.id, name=item.name, price=item.price, image_url=item.image_url, desc=item.desc,
                           tag=tag)
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


@app.route('/items', methods=['GET', 'PUT', 'POST', 'DELETE'])
def items():
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
            return jsonify(id=item.id, name=item.name, price=item.price, image_url=item.image_url, desc=item.desc,
                           tag=tag)
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


@app.route('/gallery', methods=['GET'])
def gallery():
    with db_session.create_session() as session:
        session: Session
        if request.method == 'GET':
            gallery_id = request.json['id']
        items_: List[Item] = session.query(Item).all()
        return jsonify(status="ok", message="get all items"), 202


if __name__ == "__main__":
    db_session.global_init(FILENAME_DB)
    app.run(host="127.0.0.1", port=5000)
