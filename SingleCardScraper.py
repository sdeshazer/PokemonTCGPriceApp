# scrapes a cards details
# gets current price data and history along with a higher
# resolution image.
# only scrapes a single card to which the user chooses from their search
# this avoids the case of too many requests at one time
# should there ever be an issue with too mant chrome instances being open
# windows: run Taskkill /IM chrome.exe /f

import sys
import urllib.request
from bs4 import BeautifulSoup
import csv

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import json


# browser = webdriver.Chrome(executable_path='chromedriver.exe')


option = webdriver.ChromeOptions()
option.add_argument('headless') # allow driver to work within the background
browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=option)
url = 'https://www.tcgplayer.com/product/250324/pokemon-celebrations-classic-collection-rockets-zapdos?Language=English'
csv_path_current_card = 'currentCard.csv'
language = '?Language=English'


# takes in a url from the database on the card, this is done when the user clicks on an image:

def scrape_card_details(card_details_page):
    with open(csv_path_current_card, 'w', newline="") as csv_file:
        browser.get(url)
        # browser.find_element(By.ID, 'img')
        img_list = browser.find_elements(by=By.TAG_NAME, value='img')
        card_img_src = get_card_img(img_list)
        print("image retrieved:")
        print(card_img_src)


def get_card_img(img_list):
    for img in img_list:
        img_src = img.get_attribute('src')
        if img_src.__contains__("product-images"):
            return img_src


#  priceOverTime: [{date:"2020-01-04", price:"0.04"},{date:"2020-02-04", price:"0.05"}
# price-guide-modal modal__component modal__component__scrollable
# returns only the card image we need:
# latest-sales price-guide-modal__latest-sales

def get_card_price_history():
    try:
        print("please wait page is loading....")
        webdriver.Chrome.implicitly_wait(browser, time_to_wait=5)
        element = browser.find_element(by=By.CLASS_NAME, value="price-guide__latest-sales__more")
        elements = element.find_elements(by=By.TAG_NAME, value="span")
        for el in elements:
            el.click()
        print("please wait price data is loading....")
        webdriver.Chrome.implicitly_wait(browser, time_to_wait=5)
        # browser.implicitly_wait(browser,5)
        #  element = browser.find_element(by=By.CLASS_NAME, value="price-guide-modal__load-more")
        element = browser.find_element(by=By.CLASS_NAME, value="modal-slide__scale")
        elements = element.find_elements()
        #print("any elements : " + str(len(elements)))
        for el in elements:
            el.click()
        #elements = browser.find_elements(by=By.TAG_NAME, value="li")
        #print(len(elements))

        date_elements  = browser.find_elements(by=By.CLASS_NAME, value="date")
        price_elements = browser.find_elements(by=By.CLASS_NAME, value="price")
        date_list = []
        price_list = []
        for el in  price_elements:
            price_list.append(el.text.strip())
        for el in date_elements:
            date_list.append(el.text.strip())

        listDP = list(map(lambda x, y: "date:" + x + ',' + "price:" + y, date_list, price_list))
        # returns it as a json object for the front end:
        print("returning json object of price history\n", json.dumps(listDP))
        return json.dumps(listDP)

    except Exception as e:
        print("err: closing chrome driver process with exit : " + str(e))
        quit_browsing()

# python does not handle exiting the processes in the background
def quit_browsing():
    browser.close()
    browser.quit()

# test single card scraper:
if __name__ == '__main__':
    try:
        scrape_card_details(url)
        get_card_price_history()
    except Exception as e:
        print("err: closing chrome driver process with exit : " + str(e))
        quit_browsing()
    quit_browsing()
