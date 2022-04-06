# Samantha Deshazer
# CS454
# Assignment One - Pokemon Card Scapper.
# This assignment is used for finding pokemon card information and most recent selling prices
# based on the card set chosen - ie first edition base set, jungle, celebrations.
import sys
import urllib.request
from bs4 import BeautifulSoup
import csv

csv_path_all_cards = 'index.csv'
csv_path_expensive_cards = 'pkcardsExpensive'
Prices = [10.00, 100.00, 150.00, 200.00, 300.00, 400.00, sys.float_info.max]

# collection of all the series we are interested in:
COLLECTION_SIZE = 81


# assigns series name by number.
def get_next_series(series_number):
    series = {
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
    return series.get(series_number, 'default series value error')


# gets the series name based on current series number.
def grab_series(source, series_number):
    series = get_next_series(series_number)
    print(series)
    source = 'https://shop.tcgplayer.com/price-guide/pokemon/' + series
    return source


# this function is here for later project expansion,
# where csv path can be changed or parsed from a text file.
def scape_all_series_of_interest(source, series_number):
    csv_path = csv_path_all_cards
    scrape_cards(source, series_number, csv_path)


# function for opening our data base for writing and getting our main xml to parse.
def scrape_cards(source, series_number, csv_path):
    with open(csv_path, 'w', newline="") as csv_file:
        source = grab_series(source, series_number)
        series = get_next_series(series_number)
        while series_number < COLLECTION_SIZE:
            page = urllib.request.urlopen(source)
            soup = BeautifulSoup(page, 'html.parser')
            attr = soup.find('table', class_="priceGuideTable tablesorter")
            print(source)
            get_Cards(series_number, attr, series, csv_file, )
            series_number = series_number + 1
            series = get_next_series(series_number)
            source = grab_series(source, series_number)
        print(source)


# gets card data from webpage based on xml, yes they labeled sections even and odd, unfortunately.
# so I combined them into one result list.
def get_Cards(series_number, collection, series, csv_file):
    writer = csv.writer(csv_file)
    writer.writerow(["series id", "Name", "Rarity", "Price", "Image"])
    card_collection_odd = collection.findAll('tr', class_="odd")
    card_collection_even = collection.findAll('tr', class_="even")
    card_collection = card_collection_even + card_collection_odd
    for card in card_collection:
        card_name = card.find('div', class_="productDetail")
        card_rarity = card.find('td', class_="rarity")
        card_price = card.find('td', class_="marketPrice")
        card_image = card.find('img')
        write_data(series_number, writer, card_name.text.strip(), card_rarity.text.strip(), card_price.text.strip(),
                   card_image.get('src'))


# writes card data to database
def write_data(series_number, writer, card_name, card_rarity, card_price, card_image):
    writer.writerow([series_number, card_name, card_rarity, card_price, card_image])


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
                ['Series/Set', 'Name', 'Price(>' + str(price_query) + '<' + str(Prices[index + 1]) + ')', 'Image'])
            csv_dict_reader = csv.reader(csv_file_read)
            for row in csv_dict_reader:
                for col in csv_dict_reader:
                    price_is_expensive = is_expensive(col[3], price_query, index)
                    if price_is_expensive:
                        series = get_next_series(int(col[0]))
                        writer.writerow([series, col[1], col[3], col[4]])


# main:
if __name__ == '__main__':
    source = 'https://shop.tcgplayer.com/price-guide/pokemon/'  # base source to parse
    series_number = 0  # begin with the first set or series of interest.
    scrape_again = True

    if scrape_again:
        print("scraping tcg player for card series of interest:")
        print("Populating csv file by series...")
        scape_all_series_of_interest(source, series_number)
        print("Scrape complete.")
    i = 0
    for price_query in Prices:
        if price_query < sys.float_info.max:
            print("Filtering CSV by price query: > $" + str(price_query))
            csv_path_export = csv_path_expensive_cards + '-' + str(price_query) + '.csv'
            read_write_expensive_cards(csv_path_all_cards, csv_path_export, price_query, i)
            i = i + 1
            print("Search complete.")
            print("Please refer to index.csv and pkcardsExpensive.csv files.")