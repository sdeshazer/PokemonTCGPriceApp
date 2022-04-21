# creating the tuple based on schema:
def createPokemonTuple(data):
    result_tuple = (data['set'],
                    data['name'],
                    data['rarity'])
    return (result_tuple)