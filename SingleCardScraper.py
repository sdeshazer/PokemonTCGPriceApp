# scrapes a cards details
# gets current price data and history along with a higher
# resolution image.
# only scrapes a single card to which the user chooses from their search
# this avoids the case of too many requests at one time
# should there ever be an issue with too mant chrome instances being open
# windows: run Taskkill /IM chrome.exe /f


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


option = webdriver.ChromeOptions()
option.add_argument('headless')  # allow driver to work within the background
browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=option)
language = '?Language=English'


# this function runs first from the front end, so we only need to use the parameter here:
# takes in a url from the database on the card, this is done when the user clicks on an image:
def scrape_card_details(card_details_page):
    browser.get(card_details_page)
    img_list = browser.find_elements(by=By.TAG_NAME, value='img')
    card_img_src = get_card_img(img_list)
    print("image retrieved:")
    print(card_img_src)
    return card_img_src


def get_card_img(img_list):
    try:
        for img in img_list:
            img_src = img.get_attribute('src')
            if img_src.__contains__("product-images"):
                return img_src
    except Exception as e:
        print("err: closing chrome driver process with exit : " + str(e))
        quit_browsing()


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
        # print("any elements : " + str(len(elements)))
        for el in elements:
            el.click()
        # elements = browser.find_elements(by=By.TAG_NAME, value="li")
        # print(len(elements))

        date_elements = browser.find_elements(by=By.CLASS_NAME, value="date")
        price_elements = browser.find_elements(by=By.CLASS_NAME, value="price")
        date_list = []
        price_list = []
        for el in price_elements:
            price_list.append(el.text.strip())
        for el in date_elements:
            date_list.append(el.text.strip())

        i = 0
        result_list = []
        while i < len(date_list):
            clean_date = date_list[i].replace("/", "-")
            price = price_list[i]
            if price.startswith("$"):
                price = price[1:]

            new_dict = {"date": clean_date, "price": price}
            result_list.append(new_dict)
            i += 1
        return result_list

    except Exception as e:
        print("err: closing chrome driver process with exit : " + str(e))
        quit_browsing()
    quit_browsing()


# python does not handle exiting the processes in the background
def quit_browsing():
    browser.close()
    browser.quit()
