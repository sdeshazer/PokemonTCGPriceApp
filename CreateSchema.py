from whoosh.fields import *

# schema defined here:
class PokemonCardSchema(SchemaClass):
    set = TEXT(stored=True)
    name = TEXT(stored=True)
    rarity = TEXT(stored=True)
   # price = TEXT(stored=True)