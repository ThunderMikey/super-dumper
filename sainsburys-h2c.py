#!/usr/bin/env python3
import csv, re, argparse
from bs4 import BeautifulSoup as bs


parser = argparse.ArgumentParser(description='Sainsbury\'s order, HTML list to CSV processor')
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
items = html.find('ul')

def get_name_price_quantity(row):
	name = row.find('div', class_='productDescription').find('p').text
	price = re.findall('\d+\.\d+', row.find('p', class_='cost').text)[0]
	quantity = re.findall('\d+',
		row.find('div', class_='productDetails').find('p', string=re.compile("Quantity")).text)[0]
	item_info = [name, price, quantity]
	return [info.strip() for info in item_info]

data = [get_name_price_quantity(row) for row in items.find_all('li')]
csvFile = open(csvFileName,'w')
w = csv.writer(csvFile)
w.writerows(data)

csvFile.close()
