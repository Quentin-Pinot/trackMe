# coding: utf-8

import sys
import psycopg2
from Scrapeur import Scrapeur
from Item import Item
from Mail import Mail

try:
    print("Beginning of the script dayli scrapper")

    print('Connecting to the PostgreSQL database...')

    try:
        conn = psycopg2.connect(host="localhost", database="followMe",
                                user="postgres", password="admin", port="4321")
        conn.autocommit = True
        cur = conn.cursor()
    except Exception as error:
        print("Error to connect to the database ->")
        print(error)

    print('Connected to the PostgreSQL database')

    try:
        cur.execute(
            "SELECT i.id_item, i.id_user, i.prix, i.url, i.title, u.mail \
                FROM item i, utilisateur u \
                    WHERE u.id_user = i.id_user")
    except Exception as error:
        print("Error to select every item from database ->")
        print(error)
        
    allItems = cur.fetchall()
    
    print("Start the scrapping for each items")
    
    for item in allItems:
        try:
            scraping = Scrapeur(item[3])
            scraping.check_Info()
        except Exception as error:
            print("Error in the scrapper ->")
            print(error)
        
        print("The scrapping is completed for the item '" + str(item[0]) + "'")
        print("Old price : " + str(item[2][len(item[2])-1]) + "\nNew price : "+ str(scraping.price))

        if (item[2][len(item[2])-1] > scraping.price):
            mail = Mail(item[5])
            mail.send_mail(item[4], str(item[2][len(item[2])-1]), str(scraping.price), item[3])

            print("Updating of the price for " + str(item[0]) + " in the database...")

            query = ("UPDATE item " +
             "SET prix = array_append(prix, " + str(scraping.price) + ")" +
             " WHERE id_item = " + str(item[0]))
            cur.execute(query)

        elif(item[2][len(item[2])-1] < scraping.price):
            print("Updating of the price for " + str(item[0]) + " in the database...")
            
            query = ("UPDATE item " +
             "SET prix = array_append(prix, " + str(scraping.price) + ")" +
             ", date_Updated = CURRENT_DATE" + 
             " WHERE id_item = " + str(item[0]))
            cur.execute(query)

    cur.close()
    conn.close()
except Exception as error:
    print("Error du script scrapper journalier ->")
    print(error)