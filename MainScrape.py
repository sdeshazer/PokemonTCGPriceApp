# Samantha Deshazer
# CS454
# Assignment One - Pokemon Card Scapper.
# This assignment is used for finding pokemon card information and most recent selling prices
# based on the card set chosen - ie first edition base set, jungle, celebrations.
import sys
import urllib.request
from bs4 import BeautifulSoup
import csv

# TODO scrape images / price history
csv_path_all_cards = 'index.csv'
csv_path_expensive_cards = 'pkcardsExpensive'
Prices = [10.00, 100.00, 150.00, 200.00, 300.00, 400.00, sys.float_info.max]

# collection of all the series we are interested in:
COLLECTION_SIZE = 80
language = '?Language=English'

# assigns series name by number.
def get_next_set(set_number):
    set_name = {
        0: 'swsh08-fusion-strike',
        1: 'celebrations',
        2: 'celebrations-classic-collection',
        3: 'swsh07-evolving-skies',
        4: 'swsh06-chilling-reign',
        5: 'swsh05-battle-styles',
        6: 'first-partner-pack',
        7: 'shining-fates',
        8: 'shining-fates-shiny-vault',
        9: 'swsh04-vivid-voltage',
        10: 'swsh01-sword-and-shield-base-set',
        11: 'skyridge',
        12: 'sandstorm',
        13: 'ruby-and-sapphire',
        14: 'expedition',
        15: 'gym-challenge',
        16: 'gym-heroes',
        17: 'swsh09-brilliant-stars',
        18: 'base-set',
        19: 'xy-fates-collide',
        20: 'sm-burning-shadows',
        21: 'sm-unbroken-bonds',
        22: 'sm-forbidden-light',
        23: 'sm-ultra-prism',
        24: 'sm-crimson-invasion',
        25: 'sm-base-set',
        26: 'xy-promos',
        27: 'sm-guardians-rising',
        28: 'sm-promos',
        29: 'xy-evolutions',
        30: 'xy-steam-siege',
        31: 'xy-breakthrough',
        32: 'xy-breakpoint',
        33: 'xy-ancient-origins',
        34: 'plasma-freeze',
        35: 'plasma-storm',
        36: 'plasma-blast',
        37: 'boundaries-crossed',
        38: 'noble-victories',
        39: 'emerging-powers',
        40: 'black-and-white',
        41: 'undaunted',
        42: 'unleashed',
        43: 'arceus',
        44: 'supreme-victors',
        45: 'legends-awakened',
        46: 'great-encounters',
        47: 'crystal-guardians',
        48: 'emerald',
        49: 'team-magma-vs-team-aqua',
        50: 'team-rocket',
        51: 'fossil',
        52: 'base-set-shadowless',
        53: 'firered-and-leafgreen',
        54: 'majestic-dawn',
        55: 'black-and-white-promos',
        56: 'legend-maker',
        57: 'nintendo-promos',
        58: 'power-keepers',
        59: 'team-rocket-returns',
        60: 'rising-rivals',
        61: 'mysterious-treasures',
        62: 'hidden-legends',
        63: 'kalos-starter-set',
        64: 'ex-battle-stadium',
        65: 'wotc-promo',
        66: 'legendary-collection',
        67: 'aquapolis',
        68: 'dragon',
        69: 'deoxys',
        70: 'dark-explorers',
        71: 'xy-primal-clash',
        72: 'double-crisis',
        73: 'dragon-majesty',
        74: 'sm-unified-minds',
        75: 'hidden-fates-shiny-vault',
        76: 'hidden-fates',
        77: 'champions-path',
        78: 'swsh-sword-and-shield-promo-cards',
        79: 'swsh02-rebel-clash',
        80: 'sm-cosmic-eclipse'
    }
    return set_name.get(set_number, 'default series value error')


# gets the series name based on current series number.
def grab_series(source, set_number):
    set_name = get_next_set(set_number)
    print(set_name)
    source = 'https://shop.tcgplayer.com/price-guide/pokemon/' + set_name
    return source


# this function is here for later project expansion,
# where csv path can be changed or parsed from a text file.
def scape_all_series_of_interest(source, set_number):
    csv_path = csv_path_all_cards
    scrape_cards(source, set_number, csv_path)


# function for opening our database for writing and getting our main xml to parse.
def scrape_cards(source, set_number, csv_path):
    with open(csv_path, 'w', newline="") as csv_file:
        source = grab_series(source, set_number)
        series = get_next_set(set_number)
        while set_number < COLLECTION_SIZE:
            page = urllib.request.urlopen(source)
            soup = BeautifulSoup(page, 'html.parser')
            attr = soup.find('table', class_="priceGuideTable tablesorter")
            print(source)
            get_Cards(set_number, attr, series, csv_file, )
            set_number = set_number + 1
            series = get_next_set(set_number)
            source = grab_series(source, set_number)
        print(source)


# gets card data from webpage based on xml, yes they labeled sections even and odd, unfortunately.
# so I combined them into one result list.
def get_Cards(set_number, collection, series, csv_file):
    writer = csv.writer(csv_file)
    # writer.writerow(["set", "Name", "Rarity", "Price"])
    card_collection_odd = collection.findAll('tr', class_="odd")
    card_collection_even = collection.findAll('tr', class_="even")
    card_collection = card_collection_even + card_collection_odd
    set_name = get_next_set(set_number)
    for card in card_collection:
        card_name = card.find('div', class_="productDetail")
        print("card name is of type:" + str(card_name.text.strip()))
        card_details_page = card_name.find('a')['href']
        print("card details page:" + str(card_details_page))
        card_rarity = card.find('td', class_="rarity")
        card_price = card.find('td', class_="marketPrice")
        write_data(set_name, writer, card_name.text.strip(), card_rarity.text.strip(), card_price.text.strip(), str(card_details_page))


# writes card data to database
def write_data(set_number, writer, card_name, card_rarity, card_price, card_details_page):
    writer.writerow([set_number, card_name, card_rarity, card_price, card_details_page])


def is_expensive(card_price, price_query, index):
    for character in card_price:
        if character.isdigit():
            price = card_price.replace('$', '')
            price = price.replace(',', '')
            price_number = float(price)
            if (price_number > price_query) & (price_number < float(Prices[index + 1])):
                return True


# reads the CSV database scraped and produces a separate csv of expensive cards
# based on the price_query (set in main).
def read_write_expensive_cards(csv_src, csv_des, price_query, index):
    with open(csv_src, 'r', newline="") as csv_file_read:  # reading in the cards from index.csv
        with open(csv_des, 'w', newline="") as csv_file_write:  # writing query to the new csv for our records
            writer = csv.writer(csv_file_write)
            writer.writerow(
                ['Set', 'Name', 'Price(>' + str(price_query) + '<' + str(Prices[index + 1]) + ')'])
            csv_dict_reader = csv.reader(csv_file_read)
            for row in csv_dict_reader:
                for col in csv_dict_reader:
                    price_is_expensive = is_expensive(col[3], price_query, index)
                    if price_is_expensive:
                        set = get_next_set(int(col[0]))
                        writer.writerow([set, col[1], col[3], col[4]])


# test / rescrape database:
if __name__ == '__main__':
    source = 'https://shop.tcgplayer.com/price-guide/pokemon/'  # base source to parse
    set_number = 0  # begin with the first set or series of interest.
    scrape_again = True

    if scrape_again:
        print("scraping tcg player for card series of interest:")
        print("Populating csv file by series...")
        scape_all_series_of_interest(source, set_number)
        print("Scrape complete.")
    i = 0
    for price_query in Prices:
        if price_query < sys.float_info.max:
            print("Filtering CSV by price query: > $" + str(price_query))
            csv_path_export = csv_path_expensive_cards + '-' + str(price_query) + '.csv'
            # read_write_expensive_cards(csv_path_all_cards, csv_path_export, price_query, i)
            i = i + 1
            print("Search complete.")
            print("Please refer to index.csv and pkcardsExpensive.csv files.")
