#!/usr/bin/env python

import re, sys, time

from bs4 import BeautifulSoup
import psycopg2
from selenium import webdriver

bid_history = []

class Item():
    # contains all information about an item
    # name, id, link, winner, win price, actual price, bid history

    def __init__(self, link):
        self.link = link
        self.driver = webdriver.PhantomJS()
        self.bid_count = 0
        self.name = None
        self.attributes = {
            'winner':None,
            'win_price':None,
            'actual_price':None,
            'bid_history':[]
        }

    def pretty_print(self):
        print 'Name: ' + self.name
        print 'Link: ' + self.link
        print 'Winner: ' + self.attributes['winner']
        print 'Win Price: ' + str(self.attributes['win_price'])
        print 'Actual Price: ' + str(self.attributes['actual_price'])

        for bid in self.attributes['bid_history'][-10:]:
            print 'Bid No. ' + str(bid['id'])
            print 'User: ' + bid['bidder']
            print 'Price: ' + str(bid['price'])
            print 'Method: ' + bid['method']
            print 'Auction Time: ' + bid['auction_time']
            print 'Retrieval Time: ' + bid['retrieval_time']


    def watch(self):
        # loops over the item page checking if new bids have been made
        # adds them to the item's bid_history attribute

        while(True):
            html = self.driver.page_source
            retrieval_time = time.strftime("%d-%b-%Y %H:%M:%S", time.localtime())
            soup = BeautifulSoup(html, 'html.parser')

            try:
                if soup.find('p', {'class':'won_price'}):
                    winner = soup.find('span', {'class':'won_username'}).string
                    final_price = soup.find('p', {'class':'won_price'}).string

                    if bool(re.search(r'\d', final_price)):
                        final_price = float(final_price.strip()[1:])
                        actual_price = float(soup.find('ul', {'class':'price-breakdown'}).find('span', {'class':'float-right'}).string.strip()[1:])

                        self.attributes['winner'] = winner
                        self.attributes['win_price'] = final_price
                        self.attributes['actual_price'] = actual_price
                        print 'auction over'
                        self.driver.quit()
                        break
                else:
                    bids = soup.find('table', {'id':'bid-history'}).find_all('tr')[:2]

                    for x in bids[::-1]:
                        elements = x.find_all('td')

                        if re.search(r'\d', elements[2].string):
                            bid = {
                            'id':self.bid_count,
                            'bidder':elements[1].string,
                            'price':float(elements[2].string.strip()[1:]),
                            'method':elements[3].string,
                            'auction_time':'historic',
                            'retrieval_time':'historic'
                            }

                        if not any(b['price'] == bid['price'] for b in self.attributes['bid_history']):
                            self.attributes['bid_history'].append(bid)
                            self.bid_count+=1
                time.wait(2)
            except AttributeError:
                pass


    def store(self):
        # stores all information including all past bids

        try:
            conn = psycopg2.connect("dbname=items user=jakelaboss host='ec2-54-234-158-224.compute-1.amazonaws.com' password='~r@mnUHPWv)00Cbju:?e<WM5q~2EBaeP'")
            cur = conn.cursor()
            sql = 'INSERT INTO bids (order, bidder, price, method, auction_time, retrieval_time) ON CONFLICT NOTHING;'
            bids = self.attributes['bid_history']

            for bid in bids:
                data = (bid['id'], bid['bidder'], bid['price'], bid['method'], bid['auction_time'], bid['retrieval_time'])
                cur.execute(sql, data)

        except psycopg2.DatabaseError, e:
            print 'Error %s' % e
            sys.exit(1)
        finally:
            conn.commit()
            conn.close()

    def start(self):
        # starts inspection of item by collecting on information on the page
        # usually before the majority of bids have been placed

        try:
            self.driver.get(self.link)
        except Exception, e:
            print 'Error opening site: ', e

        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        self.name = soup.find('h1', {'id':'product_title'}).string

        bids = soup.find('table', {'id':'bid-history'}).find_all('tr')

        for bid in bids[::-1]:
            elements = bid.find_all('td')

            if re.search(r'\d', elements[2].string):
                bid = {
                    'id':self.bid_count,
                    'bidder':elements[1].string,
                    'price':float(elements[2].string.strip()[1:]),
                    'method':elements[3].string,
                    'auction_time':'historic',
                    'retrieval_time':'historic'
                    }

                self.attributes['bid_history'].append(bid)
                self.bid_count+=1
