import csv
import datetime
import sys
import time
from pathlib import Path

import requests
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By

from driver import Driver


def scrape(term = "biology"):
    return


if __name__ == "__main__":
    import random
    from urllib.request import Request, urlopen


    url="https://svnweb.freebsd.org/csrg/share/dict/words?revision=61569&view=co"
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})

    web_byte = urlopen(req).read()

    webpage = web_byte.decode('utf-8')
    slice = webpage.split("\n")
    random.shuffle(slice)
    
    driver = Driver()
    n = 10
    while n > 0:
        word = slice[n]
        if len(word) < 3:
            continue
        n -= 1
        print(f"Scraping word: {word}")
        driver.scrape_term(word)
    
    driver.dump_results()

    
        # r = requests.get('https://ankiweb.net/shared/decks/biology')
        # print(r.text) # any difference to r.content?