#!/usr/bin/env python3
import csv, re, argparse
from bs4 import BeautifulSoup as bs
from shared_py.funcs import get_the_only_element

def get_name_price_quantity(row):
    try:
        name = row.find('h3').find('a').text
    except AttributeError as err:
        print("can't find name")
        print(err)
        print(row)
        exit(1)
    try:
        price_match = re.findall(
                '\d+\.\d+',
                row.find('div', class_='price-control-wrapper').find('span', class_='value').text
                )
    except AttributeError as err:
        print("can't find price")
        print(err)
        print(row)
        exit(1)
    try:
        quantity_match = re.findall(
                '\d+',
                row.find('input', class_='product-input')['value']
                )
    except AttributeError as err:
        print("can't find quantity")
        print(err)
        print(row)
        exit(1)
    price = get_the_only_element(price_match)
    quantity = get_the_only_element(quantity_match)
    total_price = float(price) * float(quantity)
    item_info = [name, str(total_price), quantity]
    return [info.strip() for info in item_info]

def filter_items(html):
    items = get_the_only_element(html.find_all('ul', class_='product-list'))
    return items.find_all('li', recursive=False)
