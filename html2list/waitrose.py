#!/usr/bin/env python3
import csv, re, argparse
from bs4 import BeautifulSoup as bs
from functools import reduce
import operator


parser = argparse.ArgumentParser(description='Waitrose order, HTML list to CSV processor')
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
orderDetails = html.find('div', id='order-details')

def get_the_only_element(l):
    if len(l) != 1:
        raise RuntimeError("matched more than one element!\n", l)
    else:
        return l[0]

def get_name_price_quantity(row):
    tds = row.find_all('td')
    try:
        # first td
        name = tds[0].text
        # the 4th td
        quantity = get_the_only_element(
                re.findall('\d+',
                    tds[3].text
                    )
                )
        # the 5th td
        price = get_the_only_element(
                re.findall('\d+\.\d+',
                    tds[4].text)
                )
    except AttributeError as err:
        print(err)
        print(row)
        exit(1)
    item_info = [name, price, quantity]
    return [info.strip() for info in item_info]

orderBody = orderDetails.find_all('tbody')
orderItemLists = map(lambda x: x.find_all('tr'), orderBody)
items = reduce(operator.add, orderItemLists)

data = [get_name_price_quantity(row) for row in items]
csvFile = open(csvFileName,'w')
w = csv.writer(csvFile)
w.writerows(data)

csvFile.close()
