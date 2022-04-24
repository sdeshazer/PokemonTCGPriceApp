# displaying results in console:
def printPokemonSearchResults(query):
    header = ['SET', 'NAME', 'CARD_ID', 'RARITY', 'PRICE', 'IMAGE']
    for item in header:
        print(item.ljust(80), end='')
    print('')

    for item in query:
        for i in item:
            print(i.ljust(80), end='')
        print('')
    print('\n')