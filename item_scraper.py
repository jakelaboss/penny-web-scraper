#!/usr/bin/env python

import re
import sys
import time

from bs4 import BeautifulSoup
from selenium import webdriver

bid_history = []

class Item():
    # contains all information about an item
    # name, id, link, winner, win price, actual price, bid history

    def __init__(self, name, link):
        self.name = name
        self.link = link
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


def chck(driver, count, item):
    while(True):
        html = driver.page_source
        retrieval_time = time.strftime("%d-%b-%Y %H:%M:%S", time.localtime())
        soup = BeautifulSoup(html, 'html.parser')

        try:
            if soup.find('p', {'class':'won_price'}):
                winner = soup.find('span', {'class':'won_username'}).string
                final_price = soup.find('p', {'class':'won_price'}).string

                if bool(re.search(r'\d', final_price)):
                    final_price = float(final_price.strip()[1:])
                    actual_price = float(soup.find('ul', {'class':'price-breakdown'}).find('span', {'class':'float-right'}).string.strip()[1:])

                    item.attributes['winner'] = winner
                    item.attributes['final_price'] = final_price
                    item.attributes['actual_price'] = actual_price
                    print 'auction over'
                    driver.quit()
                    break
            else:
                latest_bidder = soup.find('td', {'id':'bhu_1'}).string
                method = soup.find('td', {'id':'bht_1'}).string
                price = soup.find('td', {'id':'bhp_1'}).string
                auction_time = soup.find('p', {'class':'large-timer2'}).string

                if re.search(r'\d', price) and float(price.strip()[1:]) != 0.0:
                    bid = {
                        'id':count,
                        'bidder':latest_bidder,
                        'price':float(price.strip()[1:]),
                        'method':method,
                        'auction_time':auction_time,
                        'retrieval_time':retrieval_time
                        }

                    if not any(b['price'] == bid['price'] for b in bid_history):
                        item.attributes['bid_history'].append(bid)
                        count+=1
        except AttributeError:
            pass

    return item

def main(url):
    try:
        print 'opening browser...'
        driver = webdriver.PhantomJS()
        print 'browser opened'
        print 'retrieving url...'
        driver.get(url)
        print 'url retrieved'
    except Exception, e:
        print 'Error opening site: ', e

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    name = soup.find('h1', {'id':'product_title'}).string

    item = Item(name, url)

    bids = soup.find('table', {'id':'bid-history'}).find_all('tr')
    count = 0

    for bid in bids[::-1]:
        elements = bid.find_all('td')

        if re.search(r'\d', elements[2].string):
            bid = {
                'id':count,
                'bidder':elements[1].string,
                'price':float(elements[2].string.strip()[1:]),
                'method':elements[3].string,
                'auction_time':'historic',
                'retrieval_time':'historic'
                }

            item.attributes['bid_history'].append(bid)
            count+=1

    return chck(driver, count, item)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'python item_scaper.py <link>'
        sys.exit()
    else:
        url = sys.argv[1]

    try:
        item = main(url)
    except KeyboardInterrupt:
        print 'scraping ended'

    item.pretty_print()
