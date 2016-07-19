#!/usr/bin/env python

import re

from selenium import webdriver
from bs4 import BeautifulSoup

bid_history = []

def chck(driver):
    html = driver.page_source
    print len(html)
    soup = BeautifulSoup(html, 'html.parser')

    latest_bidder = soup.find('td', {'id':'bhu_1'}).string
    price = float(soup.find('span', {'class':'price'}).string.strip()[1:])

    bid = {'bidder':latest_bidder, 'price':price}

    if bid not in bid_history:
        bid_history.append(bid)

def main(driver):
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    name = soup.find('h1', {'id':'product_title'}).string

    bids = soup.find('table', {'id':'bid-history'}).find_all('tr')
    print len(bids)

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



if __name__ == '__main__':
    url = raw_input('Url to scrape: ')
    print 'opening browser...'
    driver = webdriver.PhantomJS()
    print 'browser opened'
    print 'retrieving url...'
    driver.get(url)
    print 'url retrieved'

    try:
        main(driver)
    except KeyboardInterrupt:
        print 'scraping ended'

    print(bid_history)
