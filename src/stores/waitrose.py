#!/usr/bin/env python3
import json
from bs4 import BeautifulSoup as bs
from functools import reduce
import operator
from shared_py.funcs import get_the_only_element
from shared_py.funcs import eprint

gtoe = get_the_only_element

def filter_items(html):
    """
    input: BeatufulSoup html
    output: list of BS objects, each item can be directly processed by get_name_price_quantity()
    """
    quantityPricesJson = gtoe(html.find_all('script', class_='quantity_prices')).string
    namesJson = gtoe(html.find_all('script', class_='names')).string
    quantityPrices = json.loads(quantityPricesJson)
    names = json.loads(namesJson)

    # construct names dictionary
    namesDict = {}
    for i in names['products']:
        key = i['lineNumber']
        value = i['name']
        namesDict[key] = value

    # the same PyObject, there are not multiple duplicated objects because of the assignment
    items = [(i, namesDict) for i in quantityPrices['orderLines'] ]

    return items


def get_name_price_quantity(row):
    (item, namesDict) = row
    if item['orderLineStatus'] == 'SUBSTITUTED':
        name = namesDict[item['lineNumber']] + ' SUBSTITUTED'
        try:
            price = gtoe(item['substitutes'])['price']['amount']
            quantity = gtoe(item['substitutes'])['quantity']['amount']
        except RuntimeError:
            eprint("multiple substitutes for a single item: {}".format(name))
            exit(1)
    else:
        name = namesDict[item['lineNumber']]
        price = item['price']['amount']
        quantity = item['quantity']['amount']

    adjustments = item['adjustments']
    if adjustments:
        try:
            adj = gtoe(adjustments)
        except RuntimeError:
            eprint("can only process one adjustment ATM")
            eprint("FIXME")
            exit(1)
        adjType = adj['adjustmentType']
        if adjType == 'OFFER':
            price -= adj['amount']['amount']
        else:
            eprint(name)
            eprint("{} is not an OFFER adjustment".format(adjType))
            eprint("FIXME")
            exit(1)
    else:
        # no adjustments
        pass

    return [name, price, quantity]

