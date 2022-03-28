import json
from bs4 import BeautifulSoup as bs
from functools import reduce
import operator
from shared_py.funcs import get_the_only_element
from shared_py.funcs import eprint
from shared_py.funcs import return_none_if_no_key

gtoe = get_the_only_element

def get_name_price_quantity(row):
    try:
        subst = return_none_if_no_key(row, ['pickedItem', 'substitutedItemList'])
        name = row['orderLineCustomAttributes']['webItemDescription']
        nilPicks = int(row['orderLineCustomAttributes']['nilPickQty'])
    except KeyError as e:
        eprint(e)
        eprint(row)
        exit(1)
    except Exception as e:
        eprint(e)
        eprint(row)
        exit(1)
    if nilPicks:
        assert nilPicks == int(row['quantity'])
        name += " UNAVAILABLE"
        quantity = nilPicks
        price = float(row['unit_price']) * quantity
    elif subst:
        """
            substituted
        """
        try:
            sub = gtoe(subst)
        except RuntimeError:
            eprint("FIXME")
            eprint("there is more than one item in the substitution list")
            eprint(subst)
            exit(1)
        name += ' SUBSTITUTED'
        quantity = int(sub['quantity'])
        price = float(sub['priceCharged'])
    else:
        try:
            quantity = int(row['quantity'])
            price = float(row['pickedItem']['adjustedPrice'])
        except KeyError as e:
            eprint(e)
            eprint(row)
            exit(1)
    itemInfo = [name, format(price, '.2f'), quantity]
    return itemInfo

def filter_items(html):
    jsonString = gtoe(html.find_all('script', class_='json')).string
    js = json.loads(jsonString)
    orderDetail = gtoe(js['data']['order']['payload'])

    items = orderDetail['orderLines']

    # add delivery item
    # Name: deliver fee
    # Quantity: 1
    deliveryFeeValue = orderDetail['orderSummary']['deliveryCharge']['currencyAmount']
    deliveryFeeItem = {}
    # no substitutes
    deliveryFeeItem.update({'pickedItem':
        {
            'substitutedItemList': None,
            'adjustedPrice': deliveryFeeValue
            }
        })
    # item name
    # no nil picks
    deliveryFeeItem.update(
            {'orderLineCustomAttributes':
                {
                    'webItemDescription': "Delivery fee",
                    'nilPickQty': 0
                    }
                }
            )
    deliveryFeeItem['quantity'] = 1
    deliveryFeeItem['unit_price'] = deliveryFeeValue

    items.append(deliveryFeeItem)
    return items

