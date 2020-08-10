import re
from bs4 import BeautifulSoup as bs
from functools import reduce
import operator
from shared_py.funcs import get_the_only_element

goe = get_the_only_element

def get_name_price_quantity(row):
    try:
        name = get_the_only_element(
                row.find_all('h5', class_='order-details__content-title')
                ).text
    except (AttributeError, RuntimeError) as err:
        print("error in finding name")
        print(row)
        exit(1)
    try:
        # the 4th td
        # in case 1.1Kg
        quantity = re.search(r'\d+(\.\d+)?', goe(
                    row.find_all('div', class_='order-details__quantity')
                    ).text
                    ).group(0)
    except (AttributeError, RuntimeError) as err:
        print("error in finding quantity")
        print(row)
        exit(1)
    try:
        # the 5th td
        price = re.search(r'\d+(\.\d+)?', goe(
                    row.find_all('strong', class_='order-details__total-price')
                    ).text
                    ).group(0)
    except (AttributeError, RuntimeError) as err:
        print("error in finding price")
        print(row)
        exit(1)
    item_info = [name, price, quantity]
    return [info.strip() for info in item_info]

def filter_items(html):
    def get_order_items(items, chcb):
        """
        only get Substituted, Ordered
        """
        (ch, cb) = chcb
        wantedHeader = ch.find('div', class_='order-details__order-status',
                string=re.compile("Ordered|Substitutes")
                )
        if wantedHeader:
            return items + cb.find_all('div', class_='order-details__content-container',
                    recursive=False)
        else:
            return items

    def match_right_content(tag):
        if tag.name == 'div' and tag.has_attr('class'):
            return tag['class'] == ['order-details__right-content']
        else:
            return False

    try:
        orderDetails = get_the_only_element(
                html.find_all(match_right_content)
                )
    except RuntimeError as err:
        print("error in getting orderDetials")
        print(html.find_all(match_right_content))
        exit(1)

    contentHeaders = orderDetails.find_all('div', class_='order-details__order-header')
    contentBodies = orderDetails.find_all('div', class_='order-details__order-body')

    assert len(contentHeaders) == len(contentBodies)

    chcb = zip(contentHeaders, contentBodies)
    items = reduce(get_order_items, chcb, [])
    return items

