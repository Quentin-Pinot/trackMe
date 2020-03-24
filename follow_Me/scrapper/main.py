import sys
import psycopg2
from Scrapeur import Scrapeur
from Item import Item
from Mail import Mail


conn = psycopg2.connect(host="localhost", database="followMe",
                        user="postgres", password="admin", port="4321")
cur = conn.cursor()

try:
    """cur.execute(
        "INSERT INTO item(id_item, title, prix, url, id_user) VALUES(1, 'titreTest', 100, '" + str(sys.argv[1]) + "', 1)")"""
except:
    print("couille")

cur.close()
conn.close()


"""
scraping = Scrapeur("https://www.amazon.fr/LG-Smart-Dolby-Vision-OLED55C9PLA/dp/B07QNS1LVK/ref=sr_1_3?__mk_fr_FR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=24Y19O45XVKX6&keywords=tv+oled+55+pouces+4k&qid=1584723700&sprefix=tv%2Caps%2C153&sr=8-3")

itemp_Scraped = Item(scraping.title, scraping.price, scraping.url, 'Test')

print('Connecting to the PostgreSQL database...')

conn = psycopg2.connect(host="localhost", database="followMe",
                        user="postgres", password="admin", port="4321")
cur = conn.cursor()
print('Connected to the PostgreSQL database')

cur.execute("SELECT pseudo FROM utilisateur WHERE id_user = 1").split

db_version = cur.fetchone()
print(db_version)

cur.close()
conn.close()"""
