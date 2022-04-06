from flask import Flask, render_template, url_for, request
import whoosh

from whoosh.index import create_in

from whoosh.index import open_dir
from whoosh import index
from whoosh.fields import *  # schema, text, ID
from whoosh.qparser import QueryParser
from whoosh.qparser import MultifieldParser
from whoosh import qparser

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    print("Someone is at the home page.")
    return render_template('welcome_page.html')


# used in the Hello World link :
@app.route('/my-link/')
def my_link():
    print('I got clicked!')
    return 'Click.'


@app.route('/results/', methods=['GET', 'POST'])
def results():
    global mySearcher
    if request.method == 'POST':
        data = request.form
    else:
        data = request.args

    query = data.get('searchterm')
    test = data.get('test')
    titles, description = mySearcher.search(query)
    print("You searched for: " + query)
    print("Alternatively, the second box has: " + test)

    return render_template('results.html', query=query, results=zip(titles, description))


class MyWhooshSearcher(object):
    """docstring for MyWhooshSearcher"""

    def __init__(self):
        super(MyWhooshSearcher, self).__init__()

    def search(self, queryEntered):
        title = list()
        description = list()
        with self.indexer.searcher() as search:
            query = MultifieldParser(['title', 'description'], schema=self.indexer.schema)
            query = query.parse(queryEntered)
            results = search.search(query, limit=None)

            for x in results:
                title.append(x['title'])
                description.append(x['description'])

        return title, description

    def index(self):
        # schema is the set of all possible fields in a document.
        # note: seriesid denotes the series, not the card, not a unique id per card.
        schema = Schema(seriesid=ID(stored=True), name=TEXT(stored=True), rarity=TEXT(stored=True),
                        price=TEXT(stored=True), image=TEXT(stored=True))
        # we can search documents using indexer
        # stores the schema in a directory called "myIndex":
        indexer = create_in('myPokemonIndex', schema)
        writer = indexer.writer()

        # documents we are indexing for search:
        dbfile_path = "index.csv"
        #TODO use csv reader instead of standard file reader.
        with open(dbfile_path, 'r', encoding='utf-8') as dbfile:
            for card_data in dbfile:

                writer.add_document(seriesid=card_data[:1])

            writer.add_document(content=card_data)
        # writer.add_document(id=u'1', title=u'hello there', description=u'cs hello, how are you')
        # writer.add_document(id=u'2', title=u'hello bye', description=u'nice to meetcha')
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
