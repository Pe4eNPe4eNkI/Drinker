import requests

url = "http://127.0.0.1:5000"

admin_id: int = 1
courier_id: int = 2

print("all tags:")
tags_resp = requests.get(f'{url}/tags')
print(tags_resp.content)

#user is registerd here
print()
print("register:")
print(requests.put(f'{url}/register', json={"login": "tester", "password": "test"}).content)

print()
print("login:")
auth_resp = requests.get(f'{url}/auth', json={"login": "tester", "password": "test"})
print(auth_resp.content)
acc_id = auth_resp.json()["account_id"]

print()
print("adding info: ")
print(requests.post(f'{url}/account/info', json={"account_id":acc_id, "name": "Tester", "middlename":"Laze", "surname":"Ultimate", "phone":8_000_000_0000}).content)

print()
print("get gallery")
gallery_request=requests.get(f'{url}/gallery')
print(gallery_request.content)
print("items:", gallery_request.json()["items"])

print()
print("add item:")
print(requests.put(f'{url}/items', json={
    "id": 1,
    "name": "Gigulevskoe",
    "tag_id": 1,
    "price": 1000
}).content)

print()
print("add item:")
print(requests.put(f'{url}/items', json={
    "id": 2,
    "name": "jack daniel's",
    "tag_id": 3,
    "price": 1000
}).content)

print()
print("get gallery")
gallery_request=requests.get(f'{url}/gallery')
print(gallery_request.content)
print("items:", gallery_request.json()["items"])


print("get cart id")
get_cart_id = requests.get(f'{url}/user', json={"user_id": acc_id})
cart_id = get_cart_id.json()["user"]["cart_id"]
print(get_cart_id.content)

print()
print("add beer to cart:")
beer_added = requests.post(f'{url}/user/cart', json={"cart_id": cart_id, "item_id" :1, "count": 6})
print(beer_added.content)

print()
print("add whiskey to cart:")
whiskey_added = requests.post(f'{url}/user/cart', json={"cart_id": cart_id, "item_id" :2, "count": 1})
print(whiskey_added.content)

print()
print("list cart:")
print_cart_resp = requests.get(f'{url}/user/cart', json={"cart_id": cart_id})
print(print_cart_resp.content)


print()
print("make order")