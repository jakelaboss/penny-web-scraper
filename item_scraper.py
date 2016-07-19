#!/usr/bin/env python

import re
import sys

from bs4 import BeautifulSoup
import psycopg2
from selenium import webdriver

bid_history = []

def chck(driver):
    while(True):
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        latest_bidder = soup.find('td', {'id':'bhu_1'}).string

        try:
            price = float(soup.find('span', {'class':'price'}).string.strip()[1:])
        except AttributeError:
            if soup.find('p', {'class':'won_price'}):
                final_price = float(soup.find('p', {'class':'won_price'}).string.strip()[1:])
                print 'auction over'
                break

        bid = {'bidder':latest_bidder, 'price':price}

        if bid not in bid_history:
            bid_history.append(bid)


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
                'method':elements[3].string
                }

            bid_history.append(bid)
            count+=1

    chck(driver)



if __name__ == '__main__':
    if len(sys.argv) < 1:
        print 'python item_scaper.py <link>'
        sys.exit()
    else:
        url = sys.argv[0]

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

    print(bid_history)
