import json
from shared_py.funcs import get_the_only_element
from shared_py.funcs import eprint

gtoe = get_the_only_element

def filter_items(html):
    jsonString = gtoe(html.find_all('script', class_='json')).string
    js = json.loads(jsonString)
    slot_price = js['slot_price']
    order_items = js['order_items']
    order_items.append(
        {
            "quantity": 1,
            "sub_total": slot_price,
            "product": {
                "name": "Delivery fee"
            }
        }
    )
    return order_items

def get_name_price_quantity(row):
    try:
        name = row['product']['name']
        price = row['sub_total']
        quantity = row['quantity']
    except Exception as e:
        eprint(e)
        eprint(row)
        exit(1)
    return [name, price, quantity]
