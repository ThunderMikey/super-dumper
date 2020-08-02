#!/usr/bin/env python3
import csv, re, argparse
from bs4 import BeautifulSoup as bs

parser = argparse.ArgumentParser(description='Sainsbury\'s order, HTML list to CSV processor')
parser.add_argument('--input', '-i', type=str, required=True,
        help='HTML input file.')
parser.add_argument('--output', '-o', type=str, required=True,
        help='CSV output file')
args = parser.parse_args()

htmlFileName = args.input
csvFileName = args.output

htmlFile = open(htmlFileName, 'r')
htmlText = htmlFile.read()
htmlFile.close()

html = bs(htmlText, "html.parser")

entries = html.find_all('div', class_='order-details__trolley-summary-item')
data = []
for entry in entries:
        name = entry.find_next('span').text
        price = entry.find_next('span').find_next('span').text
        quantity = entry.div.span.text.split(': ')[1]
        data.append([name, price, quantity])

csvFile = open(csvFileName,'w')
w = csv.writer(csvFile)
w.writerows(data)

csvFile.close()
