import re, json
from bs4 import BeautifulSoup as bs
from functools import reduce
import operator
from shared_py.funcs import get_the_only_element

goe = get_the_only_element

def get_name_price_quantity(row):
    product = row['product']
    try:
        name = product['name']
    except (KeyError, RuntimeError) as err:
        print("error in finding name")
        print(row)
        exit(1)
    try:
        quantity = re.search(r'\d+(\.\d+)?',
                    str(row['fopAttributes']['suggested_quantity'])
                    ).group(0)
    except (KeyError, RuntimeError) as err:
        print("error in finding quantity")
        print(row)
        exit(1)
    try:
        # the 5th td
        priceSearch = re.search(r'(?P<price>\d+(\.\d+)?)(?P<pence>p)?',
                    product['price']['currentPrice']
                    )
        if priceSearch.group('pence'):
            perItemPrice = float(priceSearch.group('price'))/100
        else:
            perItemPrice = float(priceSearch.group('price'))
    except (KeyError, RuntimeError) as err:
        print("error in finding price")
        print(row)
        exit(1)
    price = str(perItemPrice * float(quantity))
    item_info = [name, price, quantity]
    return [info.strip() for info in item_info]

def filter_items(html):
    deliveredDiv = goe(html.find_all('div', id='js-productPageFops-delivered'))
    substitutedDivs = html.find_all('div', id='js-productPageFops-substituted')
    notFullyDeliveredDivs = html.find_all('div', id='js-productPageFops-notFullyDelivered')
    assert(len(substitutedDivs)<=1) # there cannot be more than 1 substituted divs
    assert(len(notFullyDeliveredDivs)<=1) # there cannot be more than 1 not fully delivered divs
    itemHtmls = [deliveredDiv] + substitutedDivs + notFullyDeliveredDivs
    items = []
    for div in itemHtmls:
        htmlSectionJson = goe(div.find_all('script', class_='js-productPageJson'))
        jsonObj = json.loads(htmlSectionJson.string)
        for itemSection in jsonObj['sections']:
            items += itemSection['fops']

    return items
