# coding: utf-8
import requests
from bs4 import BeautifulSoup
soup = BeautifulSoup(requests.get('https://pypi.org/simple/').text)
soup.find('a')[0]
soup.find('a')
soup
soup.find('a')
soup.find('a')
soup.findall('a')
soup.find_all('a')[0]
soup.find_all('a')[1]
soup.find_all('a')[2]
soup.find_all('a')[3]
soup.find_all('a')[4]
soup.find_all('a')[4]
soup.find_all('a')[4].href
soup.find_all('a')[4].attr('href')
a= soup.find_all('a')[4]
a.attrs
a.attrs['href']
