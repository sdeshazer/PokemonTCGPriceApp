# I kept this Whoosh server example in my project and modified the search
# I wanted to make my search work with the UI but ran out of time

import csv

from flask import Flask, render_template, url_for, request
import whoosh

from whoosh.index import create_in

from whoosh.index import open_dir
from whoosh import index
from whoosh.fields import *  # schema, text, ID
from whoosh.qparser import QueryParser, OrGroup
from whoosh.qparser import MultifieldParser
from whoosh import qparser

import CreateSchema
from CreateTuple import createPokemonTuple

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    print("Someone is at the home page.")
    return render_template('welcome_page.html')


# used in the Hello World link :
@app.route('/my-link/')
def my_link():
    print('User is worried')
    return 'Your worried about the link.'


@app.route('/results/', methods=['GET', 'POST'])
def results():
    global mySearcher
    if request.method == 'POST':
        data = request.form
    else:
        data = request.args

    query = data.get('searchterm')
    test = data.get('test')
    result = mySearcher.search(query, 10)
    print("You searched for: " + query)
    print("Alternatively, the second box has: " + test)

    return render_template('results.html', query=query, results=zip(result, test))


class MyWhooshSearcher(object):
    """docstring for MyWhooshSearcher"""

    def __init__(self):
        super(MyWhooshSearcher, self).__init__()

    def openCSVFile(self):
        with open('index.csv', newline='') as file:
            reader = csv.reader(file)
            pokemonCardData = list(reader)
        return pokemonCardData

    def search(self, queryEntered, topResults):
        fields = ['set', 'name', 'rarity', 'price']
        resultList = list()
        with self.indexer.searcher() as search:
            # if using OR search i.e. "charizard"
            if queryEntered[0] == '"' and queryEntered[-1] == '"':
                queryEntered = queryEntered[1:-1]
                parser = MultifieldParser(fields, schema=self.indexer.schema, group=OrGroup)
            else:
                # whoosh uses AND search by default if not explicit:
                parser = MultifieldParser(fields, schema=self.indexer.schema)
            query = parser.parse(queryEntered)
            results = search.search(query, limit=topResults)
            for x in results:
                resultList.append(createPokemonTuple(x))

        return resultList

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
                                rarity=card_data[2])

        writer.commit()
        self.indexer = indexer


# indexer = index()
# search(indexer, 'nice')

if __name__ == '__main__':
    global mySearcher
    mySearcher = MyWhooshSearcher()
    mySearcher.index()
    # title, description = mySearcher.search('hello')
    # print(title)
    app.run(debug=True)
