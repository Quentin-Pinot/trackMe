import sys
import psycopg2
from Scrapeur import Scrapeur
from Item import Item
from Mail import Mail


print("Debut du script pour l'id_user -> '" + sys.argv[1] + "'")
print('Connecting to the PostgreSQL database...')

conn = psycopg2.connect(host="127.0.0.1", database="followMe",
                        user="postgres", password="admin", port="4321")
cur = conn.cursor()
print('Connected to the PostgreSQL database')

cur.execute(
    "SELECT url FROM item WHERE id_user = " + sys.argv[1] + "AND id_item = " + sys.argv[2])

url = cur.fetchone()[0]
print("Item a scrapper : " + url)

scraping = Scrapeur(url)
itemp_Scraped = Item(scraping.title, scraping.price, scraping.url, sys.argv[1])


cur.close()
conn.close()
