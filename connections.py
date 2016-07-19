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

def store(data):
	conn = psycopg2.connect()

	for x in range(len(data)):
		d = data.pop()
		try:
			cur = conn.cursor()
			cur.execute('INSERT INTO items(auction_id, item_id, item_name, auction_price, value_price, win_time, url, winner, user_id) VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING', (d[0], d[2], d[3], d[4], d[5], d[6], d[1]))
		except psycopg2.DatabaseError, e:
			print 'Error %s' % e
			sys.exit(1)

	conn.commit()
	conn.close()
