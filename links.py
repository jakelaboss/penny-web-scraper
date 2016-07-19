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

def dbquib():
    try:
        conn = psycopg2.connect("dbname=items user=jakelaboss host='ec2-54-234-158-224.compute-1.amazonaws.com' password='~r@mnUHPWv)00Cbju:?e<WM5q~2EBaeP'")
    except:
        print "I am unable to connect to the database."

cursor = conn.cursor()

items = item_scraper.load(open(item_scraper.py,"rb"))

cursor.execute("SELECT link FROM urls WHERE used_url = f")

while link is not none:
    link = cursor.fetchone()

conn.commit()
conn.close();
