import requests

url = "http://127.0.0.1:5000"

admin_id: int = 1
courier_id: int = 2
courier2_id: int = 3


# user is registerd here
def Register(login_, password_):
    reg = requests.put(f'{url}/register', json={"login": login_, "password": password_}).content
    return reg.json()["account_id"]


def Login(login_, password_):
    auth_resp = requests.get(f'{url}/auth', json={"login": login_, "password": password_})
    return auth_resp.json()["account_id"]


def AddInfo(acc_id_, name_, middlename_, surname_, phone_):
    addinfo_req = requests.post(f'{url}/account/info',
                                json={"account_id": acc_id_, "name": name_, "middlename": middlename_,
                                      "surname": surname_, "phone": phone_})
    return addinfo_req.json()["status"]


def AddItem(id_, name_, tag_id_, price_):
    add_req = requests.put(f'{url}/items', json={
        "id": id_,
        "name": name_,
        "tag_id": tag_id_,
        "price": price_
    })
    return add_req.json()["status"]


def GetGallery():
    gallery_request = requests.get(f'{url}/gallery')
    return gallery_request.json()["items"]


def GetCartId(user_id_):
    get_cart_id = requests.get(f'{url}/user', json={"user_id": user_id_})
    return get_cart_id.json()["cart_id"]


def AddToCart(cart_id_, item_id_, count_):
    added_resp = requests.post(f'{url}/user/cart', json={"cart_id": cart_id_, "item_id": item_id_, "count": count_})
    return added_resp.json()["status"]


def ListCart(cart_id_):
    cart_resp = requests.get(f'{url}/user/cart', json={"cart_id": cart_id_})
    return cart_resp.json()["items"]


def MakeOrder(acc_id_):
    make_order_resp = requests.put(f'{url}/order/make', json={"user_id": acc_id_, "address": "petropavlovskaya 115"})
    order_id = make_order_resp.json()["order_id"]
    return order_id


def AssignOrder(order_id_, courier_id_):
    assign_order_ = requests.post(f'{url}/order/assign', json={"order_id": order_id_, "courier_id": courier_id_})
    return assign_order_.json()["status"]


def MarkCompleted(order_id_):
    complete_order = requests.post(f'{url}/order/done', json={"order_id": order_id_})
    return complete_order.json()["status"]


def MarkFailed(order_id_):
    complete_order = requests.post(f'{url}/order/fail', json={"order_id": order_id_})
    return complete_order.json()["status"]


def GetStatus(order_id_):
    check_status = requests.get(f'{url}/order', json={"order_id": order_id_})
    return check_status.json()["order"]["status"]


def GetFreeOrders():
    get_free_orders = requests.get(f'{url}/order/free')
    return get_free_orders.json()["orders"]

# test are written here


login1 = 'u1'
password1 = 'u1'
acc_id = Register(login1, password1)
cart_id = GetCartId(acc_id)

AddItem(1, "bordo", 2, 100)
AddItem(2, "beer", 1, 10)
AddItem(3, "jack daniel's", 4, 1000)

AddToCart(acc_id, 1, 2)
AddToCart(acc_id, 3, 4)

print(ListCart(cart_id))


