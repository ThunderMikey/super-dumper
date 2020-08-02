#!/usr/bin/env python3
import csv, re, argparse
from bs4 import BeautifulSoup as bs
from functools import reduce
import operator
from shared_py.funcs import get_the_only_element

gtoe = get_the_only_element

def filter_items(html):
    """
    input: BeatufulSoup html
    output: list of BS objects, each item can be directly processed by get_name_price_quantity()
    """
    orderDetails = html.find('div', id='order-details')
    orderBody = orderDetails.find_all('tbody')
    orderItemLists = map(lambda x: x.find_all('tr'), orderBody)
    items = reduce(operator.add, orderItemLists)
    return items


def get_name_price_quantity(row):
    tds = row.find_all('td')
    try:
        # first td
        name = tds[0].text
    except AttributeError as err:
        print("error in finding name")
        print(row)
        exit(1)
    try:
        # the 4th td
        quantity = gtoe(
                re.findall('\d+',
                    tds[3].text
                    )
                )
    except AttributeError as err:
        print("error in finding quantity")
        print(row)
        exit(1)
    try:
        # the 5th td
        price = gtoe(
                re.findall('\d+\.\d+',
                    tds[4].text)
                )
    except AttributeError as err:
        print("error in finding price")
        print(row)
        exit(1)
    item_info = [name, price, quantity]
    return [info.strip() for info in item_info]

