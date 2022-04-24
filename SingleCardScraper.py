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
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# browser = webdriver.Chrome(executable_path='chromedriver.exe')


option = webdriver.ChromeOptions()
option.add_argument('headless')
browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=option)
url = 'https://www.tcgplayer.com/product/250324/pokemon-celebrations-classic-collection-rockets-zapdos?Language=English'
csv_path_current_card = 'currentCard.csv'
language = '?Language=English'


def scrape_card_details(card_details_page):
    with open(csv_path_current_card, 'w', newline="") as csv_file:
        browser.get(url)
        # browser.find_element(By.ID, 'img')
        img_list = browser.find_elements(by=By.TAG_NAME, value='img')
        print(len(img_list))
        card_img_src = get_card_img(img_list)
        print(card_img_src)


def get_card_img(img_list):
    for img in img_list:
        img_src = img.get_attribute('src')
        if img_src.__contains__("product-images"):
            return img_src


# test single card scraper:
if __name__ == '__main__':
    scrape_card_details(url)
