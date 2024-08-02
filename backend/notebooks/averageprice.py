import requests
from bs4 import BeautifulSoup
import json

def fetch_average_prices(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the section with the tables
    containers = soup.find_all('div', class_='col-md-6 col-xs-12 voffset-40')

    all_data = []
    for container in containers:
        section_title = container.find('h3', class_='section-title').text.strip()
        table = container.find('table')
        if table:
            headers = [th.text.strip() for th in table.find_all('th')]
            rows = table.find_all('tr')[1:]  # Skip header row

            data = []
            for row in rows:
                entries = [td.text.strip() for td in row.find_all('td')]
                data.append(dict(zip(headers, entries)))

            all_data.append({
                'section_title': section_title,
                'data': data
            })

    return all_data

# URL of the page with average prices
url = 'https://nigeriapropertycentre.com/market-trends/average-prices'

# Fetch average rental and sale prices
average_prices = fetch_average_prices(url)
print("Fetched average prices data:", json.dumps(average_prices, indent=2))

# Save the data to a JSON file
with open('average_prices.json', 'w') as f:
    json.dump(average_prices, f)

print("Data has been saved to average_prices.json")