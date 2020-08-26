#!/usr/bin/env python3
import csv, re, argparse
from bs4 import BeautifulSoup as bs
from shared_py.funcs import get_the_only_element
from shared_py.funcs import eprint

goe = get_the_only_element

def get_name_price_quantity(row):
    """
        When Tesco items are out of stock, price and quantity disappears
        * therefore, default to non-exit behaviour
        * and print name to stderr for later fixing
    """
    priceOrQuantityNotFound = 0
    try:
        product = goe(row.find_all('div', class_='product-tile-wrapper', recursive=False))
    except RuntimeError as err:
        print("cannot find product")
        print(err)
        print(row)
        exit(1)
    try:
        name = product.find('h3').find('a').text
    except AttributeError as err:
        print("can't find name")
        print(err)
        print(product)
        exit(1)
    try:
        price = goe(
                    re.findall(
                    '\d+\.\d+',
                    product.find('div', class_='price-control-wrapper').find('span', class_='value').text
                    )
                )
    except AttributeError as err:
        print("can't find price, default to -1")
        print(err)
        print(product)
        priceOrQuantityNotFound += 1
        price = "-1"
    try:
        quantity = goe(
                    re.findall(
                    '\d+',
                    product.find('input', class_='product-input')['value']
                    )
                )
    except TypeError as err:
        print("can't find quantity, default to 1")
        print(err)
        print(product)
        priceOrQuantityNotFound += 1
        quantity = "1"
    if priceOrQuantityNotFound: eprint(name)
    total_price = float(price) * float(quantity)
    item_info = [name, str(total_price), quantity]
    return [info.strip() for info in item_info]

def filter_items(html):
    items = goe(html.find_all('ul', class_='product-list'))
    return items.find_all('li', recursive=False)
