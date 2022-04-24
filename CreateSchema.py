from whoosh.fields import *

# schema defined here:
class PokemonCardSchema(SchemaClass):
    set = TEXT(stored=True)
    name = TEXT(stored=True)
    card_id = TEXT(stored=True)
    rarity = TEXT(stored=True)
    price = TEXT(stored=True)
    image = TEXT(stored=True)
