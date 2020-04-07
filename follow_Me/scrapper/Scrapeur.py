import requests
from bs4 import BeautifulSoup
import smtplib


class Scrapeur:

    def __init__(self, url):

        self.url = url
        self.title = str()
        self.price = 0
        self.headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0" }

    def check_Info(self):
        page = requests.get(self.url, headers=self.headers)
        
        soup = BeautifulSoup(page.content, 'html.parser')

        if (soup.find(id="productTitle") != None):
            self.title = soup.find(id="productTitle").get_text().strip().replace("'", "''")
        
        elif (soup.find("h1", {"class": "a-size-large a-spacing-micro"}) != None):
            self.title = soup.find("h1", {"class": "a-size-large a-spacing-micro"}).get_text().strip().replace("'", "''")

        elif (soup.find("h3", {"class": "a-spacing-mini"}) != None):
            self.title = soup.find("h3", {"class": "a-spacing-mini"}).get_text().strip().replace("'", "''")

        if(soup.find(id="priceblock_ourprice") != None):
            priceString = soup.find(id="priceblock_ourprice").get_text().split()
            priceJoin = ''.join(priceString)
            findVirgule = priceJoin.replace(",", ".").replace("€", "")
            self.price = float(findVirgule)

        elif (soup.find(id="priceblock_saleprice") != None):
            priceString = soup.find(id="priceblock_saleprice").get_text().split()     
            priceJoin = ''.join(priceString)
            findVirgule = priceJoin.replace(",", ".").replace("€", "")
            self.price = float(findVirgule)

        elif (soup.find("span", {"class": "a-size-medium a-color-price offer-price a-text-normal"}) != None):
            priceString = soup.find("span", {"class": "a-size-medium a-color-price offer-price a-text-normal"}).get_text().split()
            priceJoin = ''.join(priceString)
            findVirgule = priceJoin.replace(",", ".").replace("€", "")
            self.price = float(findVirgule)

        elif (soup.find("span", {"class": "a-size-small a-color-base a-text-bold"}) != None):
            priceString = soup.find("span", {"class": "a-size-small a-color-base a-text-bold"}).get_text().split()
            priceJoin = ''.join(priceString)
            findVirgule = priceJoin.replace(",", ".").replace("€", "")
            self.price = float(findVirgule)

        elif (soup.find("span", {"class": "a-color-price"}) != None):
            priceString = soup.find("span", {"class": "a-color-price"}).get_text().split()
            priceJoin = ''.join(priceString)
            findVirgule = priceJoin.replace(",", ".").replace("€", "")
            self.price = float(findVirgule)
