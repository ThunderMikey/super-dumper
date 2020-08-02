#!/usr/bin/env python3
import csv, re, argparse
from bs4 import BeautifulSoup as bs
from shared_py.funcs import get_the_only_element

goe = get_the_only_element


parser = argparse.ArgumentParser(description='Tesco order, HTML list to CSV processor')
parser.add_argument('--input', '-i', type=str, required=True,
        help='HTML input file. The top level should be <ul>')
parser.add_argument('--output', '-o', type=str, required=True,
        help='CSV output file')
args = parser.parse_args()

htmlFileName = args.input
csvFileName = args.output

htmlFile = open(htmlFileName, 'r')
htmlText = htmlFile.read()
htmlFile.close()

html = bs(htmlText, "html.parser")
items = goe(html.find_all('ul', class_='product-list'))

def get_the_only_element(l):
    if len(l) != 1:
        raise RuntimeError("matched more than one element!\n", l)
    else:
        return l[0]

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

data = [get_name_price_quantity(row) for row in items.find_all('li', recursive=False)]
csvFile = open(csvFileName,'w')
w = csv.writer(csvFile)
w.writerows(data)

csvFile.close()
