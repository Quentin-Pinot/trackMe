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

        # How to get the title
        if (soup.find(id="productTitle") != None):
            self.title = soup.find(id="productTitle").get_text().strip().replace("'", "''")
        
        elif (soup.find("h1", {"class": "a-size-large a-spacing-micro"}) != None):
            self.title = soup.find("h1", {"class": "a-size-large a-spacing-micro"}).get_text().strip().replace("'", "''")

        elif (soup.find("h3", {"class": "a-spacing-mini"}) != None):
            self.title = soup.find("h3", {"class": "a-spacing-mini"}).get_text().strip().replace("'", "''")
        
        # LDLC
        elif (soup.find("h1", {"class": "title-1"}) != None):
            self.title = soup.find("h1", {"class": "title-1"}).get_text().strip().replace("'", "''")

        # TopAchat
        elif (soup.find("h1", {"class": "fn"}) != None):
            self.title = soup.find("h1", {"class": "fn"}).get_text().strip().replace("'", "''")

        # Rue du Commerce
        elif (soup.find_all("div", {"class": "titreDescription"}) != None):
            self.title = soup.find_all("div", {"class": "titreDescription"})[0].get_text()
            print(self.title)


        # How to get the price 
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

        # LDLC
        elif (soup.find("div", {"class": "price"}) != None):
            priceString = soup.find_all("div", {"class": "price"})[3].get_text()
            findVirgule = priceString.replace("€", ".")
            self.price = float(findVirgule)

        # TopAchat
        elif (soup.find("span", {"itemprop": "price"}) != None):
            priceString = soup.find_all("span", {"itemprop": "price"})[0].get_text()
            findVirgule = priceString.replace(",", ".").replace("€", "")
            self.price = float(findVirgule)

        # Rue du Commerce
        elif (soup.find("div", {"class": "price-pricesup"}) != None):
            priceString = soup.find_all("div", {"class": "price-pricesup"})[0].get_text()
            findVirgule = priceString.replace(",", ".").replace("€", "")
            self.price = float(findVirgule)