#!/usr/bin/env python3
import csv, argparse
from bs4 import BeautifulSoup as bs
from functools import reduce
import operator
import stores.asda as asda
import stores.tesco as tesco
#import stores.sainsburys
import stores.waitrose as waitrose
import stores.ocado as ocado

store_funcs = {
        "asda"       : (asda.filter_items         , asda.get_name_price_quantity),
        "tesco"      : (tesco.filter_items        , tesco.get_name_price_quantity),
#        "sainsburys" : (sainsburys.filter_items   , sainsburys.get_name_price_quantity),
        "waitrose"   : (waitrose.filter_items     , waitrose.get_name_price_quantity),
        "ocado"      : (ocado.filter_items        , ocado.get_name_price_quantity)
        }

parser = argparse.ArgumentParser(description='HTML list to CSV processor')
parser.add_argument('--store', '-s', type=str, required=True, choices=store_funcs.keys(), help='choose a store name')
parser.add_argument('--input', '-i', type=str, required=True, help='HTML input file') 
parser.add_argument('--output', '-o', type=str, required=True, help='CSV output file')
args = parser.parse_args()

htmlFileName = args.input
csvFileName = args.output
chosenStore = args.store

(filter_items, get_name_price_quantity) = store_funcs[chosenStore]

with open(htmlFileName, 'r') as htmlFile:
    htmlText = htmlFile.read()

html = bs(htmlText, "html.parser")
data = [get_name_price_quantity(row) for row in filter_items(html)]

with open(csvFileName, 'w') as csvFile:
    w = csv.writer(csvFile)
    w.writerows(data)

