#!/usr/bin/env python

import re
import sys
import time

from bs4 import BeautifulSoup
import psycopg2
from selenium import webdriver

bid_history = []

def chck(driver, count):
    while(True):
        html = driver.page_source
        retrieval_time = time.strftime("%d-%b-%Y %H:%M:%S", time.localtime())
        soup = BeautifulSoup(html, 'html.parser')

        try:
            if soup.find('p', {'class':'won_price'}):
                final_price = soup.find('p', {'class':'won_price'}).string
                if re.search(r'\d', final_price):
                    final_price = float(final_price.strip()[1:])
                    print 'auction over'
                    print final_price
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
                        bid_history.append(bid)
                        count+=1
        except AttributeError:
            pass


def main(driver):
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    name = soup.find('h1', {'id':'product_title'}).string

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

            bid_history.append(bid)
            count+=1

    chck(driver, count)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'python item_scaper.py <link>'
        sys.exit()
    else:
        url = sys.argv[1]

    try:
        print 'opening browser...'
        driver = webdriver.PhantomJS()
        print 'browser opened'
        print 'retrieving url...'
        driver.get(url)
        print 'url retrieved'
    except Exception, e:
        print 'Error opening site: ', e

    try:
        main(driver)
    except KeyboardInterrupt:
        print 'scraping ended'
        driver.quit()

    print(bid_history)
