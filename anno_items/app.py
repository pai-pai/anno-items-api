from bson.objectid import ObjectId
from flask import Flask, request
from flask_pymongo import PyMongo
from flask_smorest import abort

from schemas import (
    ShipSchema,
    SupplySchema,
    ItemSchema,
)


MILITARY_SHIP = "Military ship"
SAILING_SHIP = "Sailing ship"
STEAM_SHIP = "Steam Ship"
SHIP_ITEMS_MAPPING = {
    MILITARY_SHIP: "Military Ships",
    SAILING_SHIP: "Sailing Ships",
    STEAM_SHIP: "Steamships",
}
SPETIAL_SHIPS = {
    "Flagship": [SHIP_ITEMS_MAPPING[MILITARY_SHIP], SHIP_ITEMS_MAPPING[SAILING_SHIP]],
    "Great Eastern": [SHIP_ITEMS_MAPPING[STEAM_SHIP]],
}


app = Flask(__name__)
app.config["MONGO_URI"] = ""
mongo = PyMongo(app)


@app.get("/ships")
def get_ships():
    ships = list(mongo.db.ships.find())
    return [ShipSchema().dump(ship) for ship in ships], 200


@app.get("/supplies")
def get_supplies():
    supplies = list(mongo.db.supplies.find())
    return [SupplySchema().dump(supply) for supply in supplies], 200


def _in_filtering(filter_values):
    return { "$in": filter_values }

def _startswith_filtering(filter_value):
    # TODO escape!
    return { "$regex": f'^"*{filter_value}', "$options": 'i' }

def _contains_filtering(filter_value):
    # TODO escape!
    return { "$regex": f"{filter_value}", "$options": 'i' }


@app.get("/items")
def get_items():
    filter_option_mapping = {
        "in": _in_filtering,
        "startswith": _startswith_filtering,
        "contains": _contains_filtering,
    }
    query = {}
    for filter_key in request.args:
        filter_phrase = filter_key.split('__')
        field = filter_phrase[0]
        if field not in ItemSchema._declared_fields:
            continue
        filter_values = request.args.getlist(filter_key)
        if len(filter_values) > 1:  # rarity=&rarity=legendary
            # filter by list of possible field values
            query[field] = filter_option_mapping["in"](filter_values)
            continue
        filter_value = filter_values[0]
        if len(filter_phrase) == 1:
            # filter by exact field value
            query[field] = filter_value
            continue
        filter_option = filter_phrase[1]
        if filter_option not in filter_option_mapping:
            continue
        # filter with other options
        query[field] = filter_option_mapping[filter_option](filter_value)
    print(">>>>\n")
    print(query)
    print("<<<<\n")
    #query = {}
    #name_startswith = request.args.get('name__startswith')
    #if name_startswith and len(name_startswith) == 1:
    #    query["name"] = { "$regex": f'^"*{name_startswith}', "$options": 'i' }
    items = list(mongo.db.items.find(query))
    return [ItemSchema().dump(item) for item in items], 200


@app.get("/ships/<string:ship_id>/items")
def get_ship_items(ship_id):
    try:
        ship = mongo.db.ships.find_one({ "_id": ObjectId(ship_id) })
        ship = ShipSchema().dump(ship)
        equipped_in = ["Ships"]
        equipped_in += SPETIAL_SHIPS.get(ship["name"], [])
        equipped_in += [SHIP_ITEMS_MAPPING[t] for t in ship["types"] if t in SHIP_ITEMS_MAPPING]
        ships = list(mongo.db.items.find({ "equipped_in": { "$in": equipped_in } }))
        return [ItemSchema().dump(ship) for ship in ships], 200
    except KeyError:
        abort(404, message="Store not found.")



# Steamships == Steam Ship
# Military Ships == Military ship
# Sailing Ships == Sailing ship
# Ships == all
