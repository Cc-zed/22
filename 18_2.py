import requests
from bs4 import BeautifulSoup

HOST = 'https://rezka.ag/'
URL = 'https://rezka.ag/?filter=popular'

HEADERS = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 OPR/82.0.4227.50',
    'Accept':
    'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
}


def get_html(url, params=''):
  r = requests.get(url, headers=HEADERS, params=params)
  return r


def get_content(html):
  soup = BeautifulSoup(html, 'html.parser')
  items = soup.find_all('div', class_='b-content__inline_item')
  cards = []
  for item in items:
    title_elem = item.find('div', class_='b-content__inline_item-title')
    if title_elem:
      title = title_elem.get_text(strip=True)
    else:
      title = None

    link = item.find('a').get('href')
    img = item.find('img').get('src')

    # Extracting details
    link_details = item.find('div', class_='b-content__inline_item-link')
    if link_details:
      details_text = link_details.get_text(strip=True)
      details = details_text.split(', ')
      if len(details) >= 3:
        year = details[0]
        type_ = details[1]
        genre = details[2]
      else:
        year = 'N/A'
        type_ = 'N/A'
        genre = 'N/A'

      if len(details) >= 4:
        authors = details[3:]
      else:
        authors = []
    else:
      year = 'N/A'
      type_ = 'N/A'
      genre = 'N/A'
      authors = []

    if title:
      card = {
          'title': title,
          'link': link,
          'img': img,
          'year': year,
          'type': type_,
          'genre': genre,
          'authors': authors
      }
    else:
      card = {
          'link': link,
          'img': img,
          'year': year,
          'type': type_,
          'genre': genre,
          'authors': authors
      }
    cards.append(card)
  return cards


def parse():
  html = get_html(URL)
  if html.status_code == 200:
    cards = get_content(html.text)
    for card in cards:
      if 'title' in card:
        print(card['link'],
              card['img'],
              card['year'],
              card['type'],
              card['genre'],
              card['authors'],
              sep='\n')
      else:
        print(
            card['link'],
            card['img'],
            card['year'], 
            card['type'],
            card['genre'],
            card['authors'],
            sep='\n')
  else:
    print('Error')


parse()
