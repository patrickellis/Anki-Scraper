import csv
import datetime
import sys
import time
from pathlib import Path

import pandas as pd
import requests
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

HEADERS = ["Title", "Ratings", "Modified", "Notes", "Audio", "Images"]

class Entry():
    "This is a row entry from an Anki table result"
    def __init__(self, row):
        self.data = {}
        self.wl_cols = HEADERS
        for key, value in row.items():
            if key in self.wl_cols:
                self.data[key] = value

    def __str__(self):
        return f'{self.data["Title"]} - {self.data["Ratings"]}'
    

class Driver():
    def __init__(self):
        opts = ChromeOptions()
        opts.add_argument("--window-size=2560,1440")
        opts.add_argument("--headless")
        self.driver = webdriver.Chrome(options=opts)
        self.processed = {}
        return
    
    def scrape_term(self, term : str):
        self.driver.get(f"https://ankiweb.net/shared/decks/{term}")

        try:
            table = WebDriverWait(self.driver, 1).until(EC.visibility_of_element_located((By.XPATH, '(//table)'))).get_attribute("outerHTML")
        except:
            return

        try:
            df1 = pd.read_html(table)[0]
            count = 0
            for entry in list(filter(self.check_valid, [Entry(row) for _, row in df1.iterrows()])):
                self.processed[entry.data["Title"]] = entry
                count += 1
            print(f"Processed {count} results for term {term}.")
        except:
            print(f"Problem parsing results for term {term}")
    
    def check_valid(self, entry : Entry):
        """ 
        Filter function to remove unwanted rows. 
        """
        if entry == None:
            return False
        
        if entry.data["Title"] in self.processed: 
            return False
        
        if sum([str(x) == "nan" for x in entry.data.values()]) > 1:
            return False

        return True

    def dump_results(self):
        if len(self.processed) == 0:
            raise ValueError("No results processed!")
        
        
        rows = [HEADERS]

        for v in sorted(self.processed.values(), key=lambda x: x.data["Ratings"]):
            rows.append([str(v.data[i]) for i in v.wl_cols])

        with open("decks.csv", "w") as f:
            writer = csv.writer(f)
            writer.writerows(rows)