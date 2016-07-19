#!/usr/bin/env python

from selenium import webdriver
from bs4 import BeautifulSoup

bid_history = []

def main(driver):
    html = driver.page_source
    print len(html)
    soup = BeautifulSoup(html, 'html.parser')

    latest_bidder = soup.find('td', {'id':'bhu_1'})
    price = soup.find('span', {'class':'price'})

    bid = {'bidder':latest_bidder.string, 'price':price.string}

    if bid not in bid_history:
        bid_history.append(bid)

if __name__ == '__main__':
    url = raw_input('Url to scrape: ')
    print 'opening browser...'
    driver = webdriver.PhantomJS()
    print 'browser opened'
    print 'retrieving url...'
    driver.get(url)
    print 'url retrieved'

    while 1:
        try:
            main(driver)
        except KeyboardInterrupt:
            print 'scraping ended'
            break

    print(bid_history)
