import time
import psycopg2
import sys
import multiprocessing as mp
import item_scraper
import connections

from bs4 import BeautifulSoup, SoupStrainer
from selenium import webdriver

domain = 'http://www.quibids.com/en'
links=[]
used_links=[]
data=[]
password=[]
insert = "INSERT INTO urls(domain, url, item_id, item_name) VALUES(%s, %s, %s, %s)"

def getlink():
    try:
        conn = psycopg2.connect()
    except:
        print "I am unable to connect to the database."

        cursor = conn.cursor()


cursor.execute("SELECT link FROM urls WHERE used_url = f")
link = cursor.fetchone()

conn.commit()
conn.close();
