# this is left for cleaning up my scraped database from assignemnt 1
# this goes unused for possible future use if I decide to rewrite this
# logic for the stored database later.

import csv


def openCSVFile():
    with open('index.csv', newline='') as file:
        reader = csv.reader(file)
        pokemonCardData = list(reader)
    return pokemonCardData


# this unsused function served me to fix my set ids to correspond to the set name
# and rewrite the set name accordingly so is just here for possible use in editing
# the CSV.
def DBEditor():
    dbfile = openCSVFile()
    print(len(dbfile))
    outfile = open('index.csv', 'w', newline='')
    writer = csv.writer(outfile)
    for tuple in dbfile:
        if tuple[0] == '0':
            tuple[0] = 'fusion strike'
            print(tuple)
            writer.writerow(tuple)
        if tuple[0] == '1':
            tuple[0] = 'celebrations'
            print(tuple)
            writer.writerow(tuple)
        if tuple[0] == '2':
            tuple[0] = 'celebrations classic'
            print(tuple)
            writer.writerow(tuple)
        if tuple[0] == '3':
            tuple[0] = 'evolving skies'
            print(tuple)
            writer.writerow(tuple)
        if tuple[0] == '4':
            tuple[0] = 'chilling reign'
            print(tuple)
            writer.writerow(tuple)
        if tuple[0] == '5':
            tuple[0] = 'battle styles'
            print(tuple)
            writer.writerow(tuple)
        if tuple[0] == '6':
            tuple[0] = 'shinning fates'
            print(tuple)
            writer.writerow(tuple)
    print(len(dbfile))
