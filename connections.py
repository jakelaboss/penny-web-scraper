import time
import psycopg2
import sys
import multiprocessing as mp
import item_scraper
from bs4 import BeautifulSoup, SoupStrainer
from selenium import webdriver

conn = psycopg2.connect("dbname=items user=jakelaboss host='ec2-54-234-158-224.compute-1.amazonaws.com' password='~r@mnUHPWv)00Cbju:?e<WM5q~2EBaeP'")
cursor = conn.cursor()
items = item_scraper.load(open(item_scraper.py,"rb"))


for item in items:
    auction_price = item[0]
    price = item[1]
    info = item[2]

    query = "INSERT INTO items(auction_id, item_id, item_name, auction_price, value_price, win_time, url, winner, user_id) VALUES (%s, %s, %s, %s, %s, %s, %s);"

    data = item_scraper(auction_price, item_id,item_name, auction_price, value_price, win_time, url, winner, user_id)

    cursor.execute(query, data)

    conn.commit()
    conn.close();
