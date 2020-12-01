def filter_items(html):
        return html.find_all('div', class_='order-details__trolley-summary-item')

def get_name_price_quantity(row):
        name = row.find_next('span').text
        price = row.find_next('span').find_next('span').find_next('span').text.strip('£')
        quantity = row.div.span.text.split(': ')[1]
        return [name, price, quantity]
