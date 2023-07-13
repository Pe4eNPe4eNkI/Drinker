from flask import Flask, Blueprint, jsonify, request
from data import db_session
from data.db_session import Session
from data.models import Account, User, Admin, AccountInfo, Card, Cart, Courier, Order, Gallery, Item
from const import FILENAME_DB
from random import randrange

app = Flask(__name__)

bp = Blueprint('api', __name__, url_prefix='/api')
app.register_blueprint(bp)


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
        new_account = Account(id=randrange(1 << 16), login=login, password=password)
        new_user = User(account_id=new_account.id)
        new_info = AccountInfo(account_id=new_account.id)
        session.add_all([new_account, new_user, new_info])
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
            return jsonify(login=acc.login, name=acc_info.name, middlename=acc_info.middlename, surname=acc_info.surname, phone=acc_info.phone)
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



@app.route('/user', methods=['POST'])
def user():
    pass


@app.route('/card', methods=['GET', 'PUT'])
def card():
    pass


@app.route('/order', methods=['GET', 'POST'])
def order():
    pass


@app.route('/cart', methods=['GET', 'POST'])
def cart():
    pass


@app.route('/items', methods=['GET', 'PUT', 'POST'])
def items():
    pass


@app.route('/make_order', methods=['PUT'])
def make_order():
    pass


@app.route('/gallery', methods=['GET', 'POST'])
def gallery():
    pass


if __name__ == "__main__":
    db_session.global_init(FILENAME_DB)
    app.run(host="127.0.0.1", port=5000)
