import requests    
from bs4 import BeautifulSoup
import re

HOST = 'https://www.olx.ua/'
URL = 'https://www.olx.ua/uk/transport/'

HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
}

class Advertisement:
    def __init__(self, html_element):
        self.html_element = html_element

    def get_mileage(self):
        text = self.html_element.get_text()
        mileage_match = re.search(r'(\d+)\s*км', text)
        if mileage_match:
            return mileage_match.group(1)

    def get_engine_capacity(self):
        text = self.html_element.get_text()
        engine_capacity_match = re.search(r'(\d+\.\d+)\s*л', text)
        if engine_capacity_match:
            return engine_capacity_match.group(1)

    def get_transmission(self):
        text = self.html_element.get_text()
        transmission_match = re.search(r'передач:\s*(.+?)Тип', text)
        if transmission_match:
            return transmission_match.group(1)

    def get_fuel_type(self):
        text = self.html_element.get_text()
        fuel_type_match = re.search(r'Вид\s*палива:\s*(.+)', text)
        if fuel_type_match:
            return fuel_type_match.group(1)

def get_html(url, params=''):
    response = requests.get(url, headers=HEADERS, params=params)
    return response

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='css-1sw7q4x')
    cars = []
    for item in items:
        title_elem = item.find_next('h6', class_='css-16v5mdi er34gjf0')
        title = title_elem.get_text() if title_elem else None

        price_elem = item.find_next('p', class_='css-10b0gli er34gjf0')
        price = price_elem.get_text() if price_elem else None

        grade_elem = item.find_next('span', class_='css-efx9z5')
        grade = grade_elem.get_text() if grade_elem else None

        link_elem = item.find_next('a', class_='css-rc5s2u')
        link = HOST + link_elem.get('href') if link_elem else None

        cars.append({
            'title': title,
            'price': price,
            'grade': grade,
            'link': link
        })
    return cars

def get_car_details(link):
    response = get_html(link)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        advertisement = Advertisement(soup)
        mileage = advertisement.get_mileage()
        engine_capacity = advertisement.get_engine_capacity()
        transmission = advertisement.get_transmission()
        fuel_type = advertisement.get_fuel_type()
        return {
            'mileage': mileage,
            'engine_capacity': engine_capacity,
            'transmission': transmission,
            'fuel_type': fuel_type
        }
    else:
        print('Error:', response.status_code)
        return None

def main():
    html = get_html(URL).text
    cars = get_content(html)
    for car in cars:
        details = get_car_details(car['link'])
        if details:
            print('Title:', car['title'])
            print('Price:', car['price'])
            print('Grade:', car['grade'])
            print('Mileage:', details['mileage'])
            print('Engine Capacity:', details['engine_capacity'])
            print('Transmission:', details['transmission'])
            print('Fuel Type:', details['fuel_type'])
            print('Link:', car['link'])
            print()

if __name__ == '__main__':
    main()
