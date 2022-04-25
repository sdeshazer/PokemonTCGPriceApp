# I kept this Whoosh server example in my project and modified the search
# I wanted to make my search work with the UI but ran out of time

import csv
import requests

from flask import Flask, render_template, url_for, request
from flask_cors import CORS
import whoosh
import json
from whoosh.index import create_in

from whoosh.index import open_dir
from whoosh import index, sorting
from whoosh.fields import *  # schema, text, ID
from whoosh.qparser import QueryParser, OrGroup
from whoosh.qparser import MultifieldParser
from whoosh import collectors
from whoosh import qparser

import CreateSchema
from CreateTuple import createPokemonTuple
from PrintResults import printPokemonSearchResults
from flask import jsonify

from SingleCardScraper import scrape_card_details, get_card_price_history

app = Flask(__name__)

cors = CORS(app)
@app.route('/', methods=['GET', 'POST'])
def index():
    print("Someone is at the home page.")
    return render_template('welcome_page.html')


# used in the Hello World link :
@app.route('/card-details/')
def card_details():
    data = request.args
    card_link = data.get('cardLink')
    img_url = scrape_card_details(card_link)
    price_history = get_card_price_history()
    card_name = data.get('name')
    set_id = data.get('setId')
    card_info = mySearcher.search_query_on_set(set_id, card_name, False)
    return jsonify(map_card_details(img_url, price_history, card_info))


def map_card_details(img_url, price_history, card_info):

    job = convert_to_json(card_info)
    listA = json.loads(job)
    listA[0]['priceOverTime'] = price_history
    listA[0]['cardImageFullRes'] = img_url
    return listA


# post request with query string goes here from front end
@app.route('/query/')
def results():
    global mySearcher

    data = request.args
    query = data.get('q')

    if data.get('setId') is not None:
        set_id = data.get('setId')
        result = mySearcher.search_query_on_set(set_id, query, False)
    else:
        result = mySearcher.search_query_once(query)
    return convert_to_json(result)


def convert_to_json(result):
    fields = ['setId', 'name', 'cardNumber', 'rarity', 'currentPrice', 'iconImage', 'cardLink']
    list_A = []
    for j in result:
        object_J = dict(zip(fields, j))
        object_J['cardId'] = strip_card_id(object_J.get('cardNumber'))
        list_A.append(object_J)

    return json.dumps(list_A)


def strip_card_id(card_num):
    return card_num[:3]


class MyWhooshSearcher(object):
    """docstring for MyWhooshSearcher"""

    def __init__(self):
        super(MyWhooshSearcher, self).__init__()

    def openCSVFile(self):
        with open('index.csv', newline='') as file:
            reader = csv.reader(file)
            pokemonCardData = list(reader)
        return pokemonCardData

    # searches all cards across all sets in the database:
    def search_query_once(self, queryEntered):
        fields = ['set', 'name', 'card_id' 'rarity', 'price', 'image', 'cardLink']
        resultList = list()
        with self.indexer.searcher() as search:
            # if using AND search i.e. "charizard"
            if queryEntered[0] == '"' and queryEntered[-1] == '"':
                queryEntered = queryEntered[1:-1]
                parser = MultifieldParser(fields, schema=self.indexer.schema)
            else:
                parser = MultifieldParser(fields, schema=self.indexer.schema, group=OrGroup)
            query = parser.parse(queryEntered)
            results = search.search(query, groupedby='set')
            for x in results:
                resultList.append(createPokemonTuple(x))

        return resultList

    # searches based on set:
    def search_query_on_set(self, setQueryEntered, queryEntered, useAnd):
        fields = ['set', 'name', 'card_id' 'rarity', 'price', 'image', 'cardLink']
        resultList = list()
        with self.indexer.searcher() as search:
            # if using AND search i.e. "charizard"
            if useAnd:
                queryEntered = queryEntered[1:-1]
                parser = MultifieldParser(fields, schema=self.indexer.schema)
            else:
                # or search:
                parser = MultifieldParser(fields, schema=self.indexer.schema, group=OrGroup)
            query = parser.parse(queryEntered)
            results = search.search(query, groupedby='set')
            for x in results:
                resultList.append(createPokemonTuple(x))
            # filter by the set selected:
            filtered_results = filter(lambda set: set[0].startswith(setQueryEntered), resultList)
        return filtered_results

    def index(self):
        schema = CreateSchema.PokemonCardSchema()
        # we can search documents using indexer
        # stores the schema in a directory called "myIndex":
        create_in('myPokemonIndex', schema)
        indexer = open_dir('myPokemonIndex')
        writer = indexer.writer()
        dbfile = self.openCSVFile()
        # documents we are indexing for search:
        for card_data in dbfile:
            writer.add_document(set=card_data[0],
                                name=card_data[1],
                                card_id=card_data[2],
                                rarity=card_data[3],
                                price=card_data[4],
                                image=card_data[5],
                                card_link=card_data[6])

        writer.commit()
        self.indexer = indexer


# indexer = index()
# search(indexer, 'nice')

if __name__ == '__main__':
    mySearcher = MyWhooshSearcher()
    mySearcher.index()
    # title, description = mySearcher.search('hello')
    # print(title)

    app.run(debug=True)
    facet = sorting.FieldFacet("set", reverse=False)
    returned_results = mySearcher.search_query_on_set('swsh08-fusion-strike', 'Pikachu', False)

    printPokemonSearchResults(returned_results)
