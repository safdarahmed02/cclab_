import json
from cart import dao
from products import Product, get_product


class Cart:
    def __init__(self, id: int, username: str, contents: list[Product], cost: float):
        self.id = id
        self.username = username
        self.contents = contents
        self.cost = cost

    @staticmethod
    def load(data):
        return Cart(
            data['id'],
            data['username'],
            [Product(**content) for content in json.loads(data['contents'])],
            data['cost']
        )


def get_cart(username: str) -> list[Product]:
    cart_details = dao.get_cart(username)
    if not cart_details:
        return []

    # Flatten contents and deserialize JSON safely
    all_contents = (json.loads(cart_detail['contents']) for cart_detail in cart_details)
    flat_contents = [item for sublist in all_contents for item in sublist]

    # Fetch products in bulk if possible, else use list comprehension
    products_list = [get_product(item_id) for item_id in flat_contents]
    return products_list


def add_to_cart(username: str, product_id: int):
    dao.add_to_cart(username, product_id)


def remove_from_cart(username: str, product_id: int):
    dao.remove_from_cart(username, product_id)


def delete_cart(username: str):
    dao.delete_cart(username)
