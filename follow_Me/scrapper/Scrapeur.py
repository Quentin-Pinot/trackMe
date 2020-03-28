import requests
from bs4 import BeautifulSoup
import smtplib


class Scrapeur:

    def __init__(self, url):

        self.url = url
        self.title = str()
        self.price = 0
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0"}

    def check_Info(self):
        page = requests.get(self.url, headers=self.headers)

        soup = BeautifulSoup(page.content, 'html.parser')

        self.title = soup.find(
            id="productTitle").get_text().strip().replace("'", "''")

        if(soup.find(id="priceblock_ourprice") != None):
            priceString = soup.find(id="priceblock_ourprice").get_text().split()
        elif (soup.find(id="priceblock_saleprice") != None):
            priceString = soup.find(id="priceblock_saleprice").get_text().split()
        
        priceJoin = ''.join(priceString)
        findVirgule = priceJoin.find(",")

        self.price = int(priceJoin[0:findVirgule])
