import requests
from bs4 import BeautifulSoup
import smtplib

WEB_BROWSER = { 
    "amazon" : 'www.amazon.',
    "ldlc" : 'www.ldlc',
    "topAchat" : 'www.topachat.',
    "fnac" : 'www.fnac.',
    "rueDuCommerce" : 'www.rueducommerce.'
    }

HEADERS = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0" }

class Scrapeur:

    def __init__(self, url):

        self.url = url
        self.title = str()
        self.price = 0


    def check_Info(self):

        # Request the item's page
        page = requests.get(self.url, headers=HEADERS)

        # Scrap the page
        soup = BeautifulSoup(page.content, 'html.parser')

        # Find the web browser first and then search the info (Title, Price)
        for key, val in WEB_BROWSER.items():

            if (val in self.url):

                # Amazon
                if (key == "amazon"):
                    # Title
                    if (soup.find(id="productTitle") != None):
                        self.title = soup.find(id="productTitle").get_text().strip().replace("'", "''")
                    
                    elif (soup.find("h1", {"class": "a-size-large a-spacing-micro"}) != None):
                        self.title = soup.find("h1", {"class": "a-size-large a-spacing-micro"}).get_text().strip().replace("'", "''")

                    elif (soup.find("h3", {"class": "a-spacing-mini"}) != None):
                        self.title = soup.find("h3", {"class": "a-spacing-mini"}).get_text().strip().replace("'", "''")


                    # Price
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
                elif (key == "ldlc"):
                    # Title
                    if (soup.find("h1", {"class": "title-1"}) != None):
                        self.title = soup.find("h1", {"class": "title-1"}).get_text().strip().replace("'", "''")

                    # Price
                    if (soup.find("div", {"class": "price"}) != None):
                        priceString = soup.find_all("div", {"class": "price"})[3].get_text()
                        findVirgule = priceString.replace("€", ".")
                        self.price = float(findVirgule)


                # TopAchat
                elif (key == "topAchat"):
                    # Title
                    if (soup.find("h1", {"class": "fn"}) != None):
                        self.title = soup.find("h1", {"class": "fn"}).get_text().strip().replace("'", "''")

                    # Price
                    if (soup.find("span", {"itemprop": "price"}) != None):
                        priceString = soup.find_all("span", {"itemprop": "price"})[0].get_text()
                        findVirgule = priceString.replace(",", ".").replace("€", "")
                        self.price = float(findVirgule)


                # Fnac
                elif (key == "fnac"):
                    # Title
                    if (soup.find_all("h1", {"class": "f-productHeader-Title"}) != None):
                        #self.title = soup.find_all("h1", {"class": "f-productHeader-Title"})[0].get_text()
                        self.title = soup.find_all("h1", {"class": "f-productHeader-Title"})[0].get_text().strip()

                    # Price
                    if (soup.find("div", {"class": "f-priceBox"}) != None):
                        priceString = soup.find_all("div", {"class": "f-priceBox"})[0].get_text()
                        findVirgule = priceString.replace("€", ".")
                        self.price = float(findVirgule)

                
                # Rue du Commerce
                elif (key == "rueDuCommerce"):
                    # Title
                    if (soup.find_all("div", {"class": "titreDescription"}) != None):
                        self.title = soup.find_all("div", {"class": "titreDescription"})[0].get_text()

                    # Price
                    if (soup.find("div", {"class": "price-pricesup"}) != None):
                        priceString = soup.find_all("div", {"class": "price-pricesup"})[0].get_text()
                        findVirgule = priceString.replace("€", ".")
                        self.price = float(findVirgule)