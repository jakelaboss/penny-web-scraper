#!/usr/bin/env python

################################################################################
#
# Quibids Scraper v1.0.0
#
#
################################################################################

import time
import psycopg2
import sys
import multiprocessing as mp
from bs4 import BeautifulSoup, SoupStrainer
from selenium import webdriver

domain = 'http://www.quibids.com/en'
links=[]
used_links=[]
data=[]

def ftch(link):
	results = []
	link = domain + link

	driver = webdriver.PhantomJS()
	driver.get(link)
	print driver.current_url
	html = driver.page_source
	soup = BeautifulSoup(html, 'html.parser')

	name = soup.find('h1', {'id':'product_title'}).string.strip()
	winner = soup.find('span', {'class':'won_username'}).string.strip()

	try:
		auction_price = float(soup.find('p', {'class':'won_price'}).string.strip()[1:])
		value_price = float(soup.find('ul', {'class':'price-breakdown'}).find('span', {'class':'float-right'}).string.strip()[1:])
	except:
		auction_price = None
		value_price = None

	win_time = soup.find('div', {'id':'end-time-disclaim'}).find_all('p', {'class':'light-grey'})[1].string.strip()

	bids = []
	table = soup.find('table', {'id':'bid-history'}).find_all('td')

	for t in table:
		s = t.string
		if s and (s != '' or s!= ' '):
			bids.append(s)

	bid_history = ','.join(bids)

	link_table = soup.find('tbody', {'id':'recently-sold-content'}).find_all('td', {'class':'auctionid'})

	for l in link_table:
		try:
			lnk = l.find('a')
			links.append(lnk['href'])
		except:
			pass

	results.extend([name, link, winner, auction_price, value_price, win_time, bid_history])

	return results


def store(data):
	conn = psycopg2.connect()

	for x in range(len(data)):
		d = data.pop()
		try:
			cur = conn.cursor()
			cur.execute('INSERT INTO test3db (name, winner, auction_price, value_price, win_time, bid_history, link) VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING', (d[0], d[2], d[3], d[4], d[5], d[6], d[1]))
		except psycopg2.DatabaseError, e:
			print 'Error %s' % e
			sys.exit(1)

	conn.commit()
	conn.close()


def main():
	driver = webdriver.PhantomJS()

	url = "http:www.quibids.com/en/auctions-completed"
	driver.get(url)
	html = driver.page_source
	soup = BeautifulSoup(html, 'html.parser').find_all('div', {'class':'auction-item-wrapper'})

	for item in soup:
		link = item.find('a')
		links.append(link['href'])

	for i in range(20000):
		link = links.pop(0)
		if link not in used_links:
			data.append(ftch(link))
			used_links.append(link)

		if len(data) == 20:
			store(data)


if __name__=='__main__':
	try:
		main()
	except KeyboardInterrupt:
		print "Interrupted"
	finally:
		if data:
			store(data)
