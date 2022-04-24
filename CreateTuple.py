# creating the tuple based on schema:
def createPokemonTuple(data):
    result_tuple = (data['set'],
                    data['name'],
                    data['card_id'],
                    data['rarity'],
                    data['price'],
                    data['image'])
    return (result_tuple)