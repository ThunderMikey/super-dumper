import csv, re
from bs4 import BeautifulSoup as bs
htmlFileName = "items.html"
csvFileName = "items.csv"

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
