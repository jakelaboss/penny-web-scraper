#!/usr/bin/env python

from selenium import webdriver
from bs4 import BeautifulSoup

bid_history = []

def chck(driver):
    html = driver.page_source
    print len(html)
    soup = BeautifulSoup(html, 'html.parser')

    latest_bidder = soup.find('td', {'id':'bhu_1'}).string
    price = soup.find('span', {'class':'price'}).string

    bid = {'bidder':latest_bidder, 'price':price}

    if bid not in bid_history:
        bid_history.append(bid)

def main(driver):
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    name = soup.find('h1', {'id':'product_title'}).string

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
