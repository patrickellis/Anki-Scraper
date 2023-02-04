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
    # init_selenium_driver()
    driver = Driver()
    driver.scrape_term("biology")
    driver.scrape_term("biology")
    driver.dump_results()