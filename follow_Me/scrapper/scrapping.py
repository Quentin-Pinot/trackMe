import sys
import psycopg2
from Scrapeur import Scrapeur
from Item import Item

try:
    idUser = sys.argv[1]
    idItem = sys.argv[2]

    print("Debut du script pour l'user -> '" +
          idUser + "' et l'item '" + idItem + "'")
    sys.stdout.flush()

    print('Connecting to the PostgreSQL database...')
    sys.stdout.flush()

    conn = psycopg2.connect(host="localhost", database="followMe",
                            user="postgres", password="admin", port="5432")
    conn.autocommit = True
    cur = conn.cursor()

    print('Connected to the PostgreSQL database')
    sys.stdout.flush()

    try:
        cur.execute(
            "SELECT url FROM item WHERE id_user = " + idUser + "AND id_item = " + idItem)
    except Exception as error:
        print("Error of python script : Get the url -> " + error)
        sys.stdout.flush()

    url = cur.fetchall()[0][0]

    print("Item a scrapper -> '" +
          idItem + "'")
    sys.stdout.flush()

    scraping = Scrapeur(url)
    scraping.check_Info()

    print("Scraping done")
    sys.stdout.flush()

    item_Scraped = Item(scraping.title, scraping.price,
                        scraping.url, idUser)

    query = ("UPDATE item " +
             "SET title = '" + str(item_Scraped.title) +
             "', prix = array_append(prix, " + str(item_Scraped.price) + ")" +
             " WHERE id_item = " + idItem +
             " AND id_user = " + str(item_Scraped.user))

    cur.execute(query)

    print("Ajout final de l'item -> id '" +
          idItem + "' du nom de : '" + item_Scraped.title + "'")
    sys.stdout.flush()

    cur.close()
    conn.close()
except Exception as err:
    print("Error of python script -> " + str(err))
    sys.stdout.flush()
