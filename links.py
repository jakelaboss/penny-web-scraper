import time
import psycopg2
import sys
import multiprocessing as mp

from bs4 import BeautifulSoup, SoupStrainer
from selenium import webdriver

domain = 'http://www.quibids.com/en'
used_links=[]
data=[]
password=[]
insert = "INSERT INTO urls(domain, url, item_id, item_name) VALUES(%s, %s, %s, %s)"

def getlink():
	results = []

	driver = webdriver.PhantomJS()
	driver.get(link)
	print driver.current_url
	html = driver.page_source
	soup = BeautifulSoup(html, 'html.parser')

itemlink = soup.find('h1', {'class':'auction-item-wrapper'}).string.strip()
print itemlink




#def insertlink():
#    try:
#        conn = psycopg2.connect(insert)
#    except:
#        print "I am unable to connect to the database."
#
#        cursor = conn.cursor()
#
#cursor.execute("SELECT link FROM urls WHERE used_url = f")
#link = cursor.fetchone()
#
#conn.commit()
#conn.close();
#
#
#def ftch(link):
#	results = []
#	link = domain + link
#
#	driver = webdriver.PhantomJS()
#	driver.get(link)
#	print driver.current_url
#	html = driver.page_source
#	soup = BeautifulSoup(html, 'html.parser')
#
#	name = soup.find('h1', {'id':'product_title'}).string.strip()
#	winner = soup.find('span', {'class':'won_username'}).string.strip()
#
#	try:
#		auction_price = float(soup.find('p', {'class':'won_price'}).string.strip()[1:])
#		value_price = float(soup.find('ul', {'class':'price-breakdown'}).find('span', {'class':'float-right'}).string.strip()[1:])
#	except:
#		auction_price = None
#		value_price = None
#
#	win_time = soup.find('div', {'id':'end-time-disclaim'}).find_all('p', {'class':'light-grey'})[1].string.strip()
#
#	bids = []
#	table = soup.find('table', {'id':'bid-history'}).find_all('td')
#
#	for t in table:
#		s = t.string
#		if s and (s != '' or s!= ' '):
#			bids.append(s)
#
#	bid_history = ','.join(bids)
#
#	link_table = soup.find('tbody', {'id':'recently-sold-content'}).find_all('td', {'class':'auctionid'})
#
#	for l in link_table:
#		try:
#			lnk = l.find('a')
#			links.append(lnk['href'])
#		except:
#			pass
#
#	results.extend([name, link, winner, auction_price, value_price, win_time, bid_history])
#
#	return results
