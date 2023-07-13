from flask import Flask, Blueprint, jsonify, request
from data import db_session
from data.models import Account, AccountInfo, Card, Cart, Courier, Order, Gallery, Item
from hashlib import sha256
app = Flask(__name__)

bp = Blueprint('api', __name__)
app.register_blueprint(bp, url_prefix="/api")


@bp.route('/auth', methods=['GET'])
def auth():
    login = request.json["login"]
    password = sha256(request.json["password"])

    with db_session.create_session() as session:
        if session.query(Account).filter(Account.login == login, Account.password == password).first():
            return jsonify(status="fail", message="incorrect login or password")
    return jsonify(status="ok", message="successful login"), 202


@bp.route('/register', methods=['PUT'])
def register():
    login = request.json["login"]
    password = sha256(request.json["password"])


@bp.route('/account', methods=['POST', 'DELETE'])
def account():
    pass


@bp.route('/account/info', methods=['GET', 'POST'])
def account_info():
    pass


@bp.route('/user', methods=['POST', 'DELETE'])
def user():
    pass


@bp.route('/admin', methods=['POST', 'DELETE'])
def admin():
    pass


@bp.route('/courier', methods=['POST', 'DELETE'])
def courier():
    pass


@bp.route('/card', methods=['GET', 'POST'])
def card():
    pass


@bp.route('/card/details', methods=['GET, POST, PUT'])
def card_details():
    pass


@bp.route('/order', methods=['GET', 'POST'])
def order():
    pass


@bp.route('/order/details', methods=['GET', 'POST'])
def order_details():
    pass


@bp.route('/cart', methods=['GET', 'POST'])
def cart():
    pass


@bp.route('/cart/details', methods=['GET, POST, PUT'])
def cart_details():
    pass


@bp.route('/items', methods=['GET'])
def items():
    pass


@bp.route('/make_order', methods=['PUT'])
def make_order():
    pass


@bp.route('/gallery', methods=['GET', 'POST'])
def gallery():
    pass


@bp.route('/gallery/details', methods=['GET', 'POST'])
def gallery_details():
    pass

