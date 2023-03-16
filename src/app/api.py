import re

from flask_pymongo import (
    ASCENDING,
    DESCENDING,
) 

from flask import (
    Blueprint,
    request,
)

from app.database import mongo
from app.schemas import (
    ShipSchema,
    SupplySchema,
    ItemSchema,
)


bp = Blueprint("api", __name__)


EQUIPPED_MAPPING = {
    "Military Ships": ["Flagship", "Military Ship"],
    "Sailing Ships": ["Flagship", "Sailing Ship"],
    "Steamships": ["Great Eastern", "Steam Ship"],
}
MILITARY_SHIP = "Military Ship"
SAILING_SHIP = "Sailing Ship"
STEAM_SHIP = "Steam Ship"
SHIP_ITEMS_MAPPING = {
    MILITARY_SHIP: "Military Ships",
    SAILING_SHIP: "Sailing Ships",
    STEAM_SHIP: "Steamships",
}
SPECIAL_SHIPS = {
    "Flagship": [SHIP_ITEMS_MAPPING[MILITARY_SHIP], SHIP_ITEMS_MAPPING[SAILING_SHIP]],
    "Great Eastern": [SHIP_ITEMS_MAPPING[STEAM_SHIP]],
}


def _get_ship_items_filters(ship_obj):
    equipped_in = ["Ships"]
    equipped_in += SPECIAL_SHIPS.get(ship_obj["name"], [])
    for ship_type in ship_obj["types"]:
        ship_type = ship_type.title()
        if ship_type in SHIP_ITEMS_MAPPING:
            equipped_in.append(SHIP_ITEMS_MAPPING[ship_type])
    return equipped_in


def _in_filtering(filter_values):
    return { "$in": filter_values }


def _startswith_filtering(filter_value):
    return { "$regex": f'^"*{filter_value}', "$options": 'i' }


def _contains_filtering(filter_value):
    return { "$regex": f"{filter_value}", "$options": 'i' }


def _construct_query(fields, params):
    filter_option_mapping = {
        "in": _in_filtering,
        "startswith": _startswith_filtering,
        "contains": _contains_filtering,
    }
    query = {}
    order = {}
    for param_key in params:
        param_raw = param_key.split('__')
        param = param_raw[0]
        param_values = params.getlist(param_key)
        if param == 'sort':
            for sort_field in param_values:
                sort_option, sort_field = re.match(r"^(-)?([\w.]+)", sort_field).groups()
                order[sort_field] = ASCENDING if sort_option is None else DESCENDING
            continue
        if param not in fields:
            # skip if passed 'param' is not in scheme's fields and it is not sort option
            continue
        if param in query:
            # skip if it was already added to filter query
            continue
        if len(param_values) > 1:  # rarity=&rarity=legendary
            # filter by list of possible field values
            query[param] = filter_option_mapping["in"](param_values)
            continue
        param_value = param_values[0]
        if len(param_raw) == 1:
            # filter by exact field value
            query[param] = param_value
            continue
        filter_option = param_raw[1]
        if filter_option not in filter_option_mapping:
            continue
        # filter with other options
        query[param] = filter_option_mapping[filter_option](param_value)
    return query, order


@bp.route("/items")
def get_items():
    # order by:
    # - Name
    # - Rarity (rarity_order)
    # -----
    # filter by:
    # - Rarity
    # -- Common
    # -- Uncommon
    # -- Rare
    # -- Epic
    # -- Legendary
    # - DLC
    # -- ...
    # - Traits
    # -- ...
    query, orderby = _construct_query(
        ('rarity', 'dlc', 'traits', 'name'),
        request.args
    )
    items = mongo.db.items.find(query, sort=list(orderby.items()) or [("name", ASCENDING)])
    rarities = mongo.db.items.aggregate([
	    {
            "$group": {
                "_id": { "rarity" : "$rarity" },
                "rarity_order": { "$first" : "$rarity_order" }
            }
        },
        { "$sort": { "rarity_order": ASCENDING } },
    ])
    dlcs = mongo.db.items.distinct("dlc")
    traits = mongo.db.items.distinct("traits")
    return {
        "objects": [ItemSchema().dump(item) for item in items],
        "_filters": {
            "rarity": [el.get("_id").get("rarity") for el in list(rarities)],
            "dlc": sorted(dlcs),
            "traits": sorted(traits),
        }
    }, 200


@bp.route("/ships")
def get_ships():
    # order by:
    # - Name
    # - Number of Slots
    # -----
    # filter by:
    # - Type
    # -- Hybrid
    # -- Military ship
    # -- Sailing ship
    # -- ...
    query, orderby = _construct_query(ShipSchema._declared_fields, request.args)
    ships = mongo.db.ships.find(query, sort=list(orderby.items()) or [("name", ASCENDING)])
    ship_types = mongo.db.ships.distinct("types")
    return {
        "objects": [ShipSchema().dump(ship) |
                    {"equipped_in": _get_ship_items_filters(ship)} for ship in ships],
        "_filters": {
            "types": sorted(ship_types)
        }
    }, 200


@bp.route("/supplies")
def get_supplies():
    # order by:
    # - Name
    # - Morale (combined_morale_per_50t)
    # -----
    # filter by:
    # - Ration Bonus
    # -- Yes
    # -- No
    # - Expedition Bonus
    # -- Crafting
    # -- Diplomacy
    # -- Faith
    # -- ...
    query, orderby = _construct_query(
        ('extra_rations', 'bonuses', 'name'),
        request.args
    )
    supplies = mongo.db.supplies.aggregate([
        { "$match": query },
        {
            "$group": {
                "_id": "$name",
                "supply": { "$first": "$$ROOT" },
                "crafting": { "$sum": "$bonuses.crafting" },
                "diplomacy": { "$sum": "$bonuses.diplomacy" },
                "faith": { "$sum": "$bonuses.faith" },
                "force": { "$sum": "$bonuses.force" },
                "hunting": { "$sum": "$bonuses.hunting" },
                "medicine": { "$sum": "$bonuses.medicine" },
                "naval_power": { "$sum": "$bonuses.naval_power" },
                "navigation": { "$sum": "$bonuses.navigation" },
            }
        },
        {
            "$replaceRoot": {
                "newRoot": {
                    "$mergeObjects": [
                        "$supply",
                        {
                            "bonuses": {
                                "crafting": "$crafting",
                                "diplomacy": "$diplomacy",
                                "faith": "$faith",
                                "force": "$force",
                                "hunting": "$hunting",
                                "medicine": "$medicine",
                                "naval_power": "$naval_power",
                                "navigation": "$navigation",
                            }
                        }
                    ]
                }
            }
        },
        { "$sort": (orderby or { "name": ASCENDING }) }
    ])
    return {
        "objects": [SupplySchema().dump(supply) for supply in supplies],
        "_filters": {},
    }, 200
