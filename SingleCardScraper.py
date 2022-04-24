# scrapes a cards details
# gets current price data and history along with a higher
# resolution image.
# only scrapes a single card to which the user chooses from their search
# this avoids the case of too many requests at one time

import sys
import urllib.request
from bs4 import BeautifulSoup
import csv

from selenium import webdriver
browser = webdriver.Chrome()

url = 'https://www.tcgplayer.com/product/250334/pokemon-celebrations-classic-collection-luxray-gl-lvx'
csv_path_current_card = 'currentCard.csv'
language = '?Language=English'

def scrape_card_details(card_details_page):
    with open(csv_path_current_card, 'w', newline="") as csv_file:
        page = urllib.request.urlopen(card_details_page)
        soup = BeautifulSoup(page, 'html.parser')
        page_attr = soup.findAll('section', class_="marketplace")
        image_attr = soup.findAll('img', class_="progressive-image-main")
        print(len(page_attr))
        print(len(image_attr))
        print(str(soup))




# test single card scraper:
if __name__ == '__main__':
    scrape_card_details(url)
