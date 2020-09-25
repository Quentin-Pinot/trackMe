# coding: utf-8

import sys
import psycopg2
from Scrapeur import Scrapeur
from Item import Item
from Mail import Mail
import logging

logging.basicConfig(filename='scrappingJournalier.log', level=logging.DEBUG)

try:
    logging.info("Beginning of the script dayli scrapper")

    logging.info('Connecting to the PostgreSQL database...')

    try:
        conn = psycopg2.connect(host="localhost", database="followMe",
                                user="postgres", password="admin", port="5432")
        conn.autocommit = True
        cur = conn.cursor()
    except Exception as error:
        logging.warning("Error to connect to the database ->")
        logging.warning(error)

    logging.info('Connected to the PostgreSQL database')

    try:
        cur.execute(
            "SELECT i.id_item, i.id_user, i.prix, i.url, i.title, u.mail \
                FROM item i, utilisateur u \
                    WHERE u.id_user = i.id_user")
    except Exception as error:
        logging.warning("Error to select every item from database ->")
        logging.warning(error)
        
    allItems = cur.fetchall()
    
    logging.info("Start the scrapping for each items")
    
    for item in allItems:
        try:
            scraping = Scrapeur(item[3])
            scraping.check_Info()

            logging.info("The scrapping is completed for the item '" + str(item[0]) + "'")
            logging.info("Old price : " + str(item[2][len(item[2])-1]) + "\nNew price : "+ str(scraping.price))
        except Exception as error:
            logging.warning("Error in the scrapper ->")
            logging.warning(error)
        


        if (scraping.price == 'Épuisé' & scraping.price != item[2][len(item[2])-1]):
            print('no')
            logging.info('Price is sold out')

            mail = Mail(item[5])
            mail.send_mail(item[4], str(item[2][len(item[2])-1]), 'SOLD OUT', item[3])

            scraping.price = 0.0

            logging.info("Updating of the price for " + str(item[0]) + " in the database...")
            
            query = ("UPDATE item " +
             "SET prix = array_append(prix, " + str(scraping.price) + ")" +
             ", date_up = CURRENT_DATE" + 
             " WHERE id_item = " + str(item[0]))
            cur.execute(query)

        elif (float(scraping.price) < float(item[2][len(item[2])-1])) & (float(scraping.price) != 0):
            mail = Mail(item[5])
            mail.send_mail(item[4], str(item[2][len(item[2])-1]), str(scraping.price), item[3])

            logging.info("Updating of the price for " + str(item[0]) + " in the database...")

            query = ("UPDATE item " +
             "SET prix = array_append(prix, " + str(scraping.price) + ")" +
              ", date_up = CURRENT_DATE" +
             " WHERE id_item = " + str(item[0]))
            cur.execute(query)

        elif(float(scraping.price) > float(item[2][len(item[2])-1])) & (float(scraping.price) != 0):
            logging.info("Updating of the price for " + str(item[0]) + " in the database...")
            
            query = ("UPDATE item " +
             "SET prix = array_append(prix, " + str(scraping.price) + ")" +
             ", date_up = CURRENT_DATE" + 
             " WHERE id_item = " + str(item[0]))
            cur.execute(query)

    cur.close()
    conn.close()
except Exception as error:
    logging.warning("Error du script scrapper journalier ->")
    logging.warning(error)